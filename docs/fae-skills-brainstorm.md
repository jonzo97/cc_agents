# FAE Skills Brainstorm

Candidate Claude Code skills for Field Application Engineers working across semiconductor product lines. Organized by product domain with cross-cutting skills at the end.

**Existing FPGA skills** (proof-of-concept): fpga-error, libero-build, fpga-search, synth-log-miner, fpga-ip-params

---

## FPGA (PolarFire, Igloo2, SmartFusion2)

**Typical workflows:** Constraint authoring, synthesis/P&R iteration, timing closure, IP configuration, design review, customer debug.

**Existing skills:** 5 (see above) — most mature domain.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| fpga-constraint-gen | Generate SDC/PDC constraints from pin assignments | Templates, clock patterns, I/O standards reference |
| fpga-timing-closure | Guided timing closure workflow: analyze violations, suggest fixes | Common fix patterns, WNS/TNS interpretation |
| fpga-migration | Port designs between FPGA families (Igloo2 → PolarFire) | Pin mapping, IP equivalents, constraint translation |

---

## Ethernet (LAN9xxx, KSZ, TSN)

**Typical workflows:** Register configuration, PHY/switch initialization sequences, MDIO/SPI register map lookups, VLAN/QoS setup, TSN stream configuration, PCB layout review for signal integrity.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| eth-register-config | Generate register initialization code from high-level config | Register maps, reset defaults, bit field descriptions |
| eth-phy-debug | Diagnose PHY link issues from register dumps | Link status decode, auto-negotiation state machine, common failure patterns |
| eth-tsn-config | Configure TSN features (802.1Qbv, Qav, AS) | Schedule calculation, gate control list generation |

---

## MCU (PIC, SAM, AVR)

**Typical workflows:** Peripheral configuration, clock tree setup, interrupt priority assignment, linker script debugging, Harmony/START code generation review, fuse/configuration bit setup, power consumption estimation.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| mcu-peripheral-config | Generate peripheral init code from requirements | Register maps, clock dependencies, pin mux tables |
| mcu-clock-calc | Calculate clock tree from target frequencies | PLL formulas, divider chains, jitter constraints |
| mcu-power-estimate | Estimate power consumption from peripheral usage | Current draw tables, duty cycle calculations |
| mcu-fuse-config | Generate configuration bit settings | Fuse maps by family, security implications, common gotchas |

---

## Analog (Power, Motor, Op-Amp)

**Typical workflows:** Component selection from parametric specs, feedback loop calculation, thermal analysis, SPICE model validation, application circuit review.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| power-design-calc | Calculate inductor/capacitor values for switching regulators | Topology formulas (buck, boost, SEPIC), component stress |
| motor-drive-config | Configure motor driver parameters from motor specs | Commutation tables, current sense calculations, protection thresholds |
| analog-part-select | Find parts matching parametric requirements | Key specs by category, comparable parts, availability notes |

---

## Security (ATECC608, Trust Platform)

**Typical workflows:** Certificate chain setup, key provisioning sequences, secure boot configuration, TLS handshake debugging, manifest file generation.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| crypto-provision | Generate provisioning scripts for ATECC608 | Slot configuration, key types, certificate templates |
| secure-boot-setup | Configure secure boot chain for a platform | Boot sequence, key storage, verification flow |
| tls-debug | Debug TLS handshake failures with crypto devices | Common failure patterns, certificate chain validation |

---

## POE (Power over Ethernet)

**Typical workflows:** Power budget calculation, PD/PSE classification, detection/classification resistor selection, thermal management for high-power ports.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| poe-power-budget | Calculate system power budget for multi-port PSE | IEEE 802.3bt classes, cable loss, power allocation |
| poe-classification | Generate classification resistor values | PD class tables, detection signatures |

---

## PCIE (Switches, Bridges)

**Typical workflows:** Topology configuration, lane allocation, bifurcation setup, link training debug, BAR allocation.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| pcie-topology | Configure switch topology from system requirements | Lane mapping, bifurcation options, bandwidth calculation |
| pcie-link-debug | Diagnose link training failures from status registers | LTSSM state decode, equalization analysis |

---

## USB (Hubs, Controllers, Type-C/PD)

**Typical workflows:** Hub configuration, PD policy setup, Type-C state machine debug, descriptor generation, compliance test prep.

**Candidates:**
| Skill Idea | What It Does | Bundle Contents |
|------------|-------------|-----------------|
| usb-pd-policy | Generate PD power contract tables | Source/sink caps, voltage/current profiles, PPS ranges |
| usb-descriptor-gen | Generate USB descriptors from requirements | Device/config/interface/endpoint descriptors, string tables |

---

## Cross-Cutting Skills (Highest ROI)

These skills serve multiple product lines — likely the best starting point after FPGA.

| Skill Idea | What It Does | Domains |
|------------|-------------|---------|
| **errata-check** | Search errata for a specific device, flag known issues in a design | All |
| **schematic-review** | Guided schematic review checklist by product type | All |
| **part-select** | Parametric search + comparison for component selection | Analog, MCU, Ethernet |
| **appnote-search** | Find relevant application notes for a design problem | All |
| **customer-debug** | Structured debug triage: symptoms → likely causes → tests | All |
| **bom-analysis** | Review BOM for EOL risk, second sources, cost optimization | All |
| **compliance-check** | Check design against relevant standards (UL, CE, FCC) | All |
| **thermal-analysis** | Estimate junction temps from power dissipation + thermal resistance | Analog, POE, FPGA |
| **design-review** | Full design review workflow combining schematic, errata, thermal | All |

---

## Priority Ranking

**Tier 1 — Build next (high frequency, high time savings, feasible):**
1. errata-check (every design needs this, data is public)
2. customer-debug (structured triage saves hours)
3. appnote-search (constant lookup task)
4. eth-register-config (repetitive, well-documented)

**Tier 2 — Build when domain work arises:**
5. mcu-peripheral-config
6. power-design-calc
7. poe-power-budget
8. usb-pd-policy

**Tier 3 — Research needed (data availability uncertain):**
9. schematic-review (needs structured checklists per product)
10. secure-boot-setup (may require NDA info)
11. pcie-topology (complex, less frequent)

---

*Created: 2026-02-24*
*Research prompt: `research/prompts/12_fae-skills-landscape.md`*
