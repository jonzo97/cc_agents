# CozoDB Episodic Memory

Schema for agent experience replay: Task > Plan > Action > Observation > Critique.

## Quick Patterns

### Define episode schema
```python
from pycozo import Client; import time
db = Client(engine='sqlite', path='./agent_memory.db')
db.run(":create episode {id: String => type: String, content: String, "
       "parent_id: String, success: Bool, created_at: Float, last_accessed_at: Float}")
# Types: task, plan, action, observation, critique
```

### Record an episode chain
```python
ts = time.time()
data = [["t1","task","Fix timing closure","",True,ts,ts],
        ["a1","action","set_max_delay 2.5ns","t1",True,ts,ts],
        ["o1","observation","WNS=0.12ns","a1",True,ts,ts],
        ["c1","critique","Relax constraints first","t1",True,ts,ts]]
db.run("?[id,type,content,parent_id,success,created_at,last_accessed_at] <- $data "
       ":put episode {id=>type,content,parent_id,success,created_at,last_accessed_at}",
       {"data": data})
```

### Query: successful critiques
```python
results = db.run("?[id, content, created_at] := episode{id, type, content, success, "
    "created_at}, type == 'critique', success == true :order -created_at :limit 5")
```

### Prune stale episodes + touch accessed ones
```python
cutoff = time.time() - (90 * 86400)  # 90 days
db.run("?[id] := episode{id, last_accessed_at}, last_accessed_at < $cutoff "
       ":rm episode {id}", {"cutoff": cutoff})
# Touch on read to prevent useful episodes from being pruned:
db.run("?[id,ts] := episode{id}, id==$eid, ts=$now "
       ":update episode {id => last_accessed_at=ts}", {"eid":"c1","now":time.time()})
```

## Gotchas
- Always set `created_at` AND `last_accessed_at` on all nodes
- Update `last_accessed_at` on query — prevents useful episodes from pruning
- Stale lessons (90+ days untouched) pollute context — prune or decay-weight
- Conflicting critiques need reconciliation: newer + higher success rate wins

## When to Use
- Agent needs to learn from past successes/failures across sessions
- Building "what worked last time for this type of task" retrieval
- Experience replay for iterative improvement loops
