# HomeNest Alignment and Consolidation Plan

**Status:** Canonical planning boundary; not part of uCode delivery sprints  
**Date:** 2026-08-20

## Identity

HomeNest is a separate household product for local media, playback, TV/DVR,
home automation, controller-first/TV interfaces, and appliance-style Linux
deployment. It is not uCode3, a uCode 2 subsystem, or part of the uCode 1/2
delivery sequence.

HomeNest may later consume shared, versioned ecosystem packages or launch
uCode experiences, but neither project is allowed to absorb the other's
runtime ownership.

## Current-tree policy

The repository contains sound product concepts alongside overlapping and
partially duplicated implementations:

- multiple console/source trees;
- Python household/media services;
- installer and Sonic variants;
- Jellyfin, playback, TV/DVR, and Home Assistant integration;
- controller-first UI and kiosk concepts;
- copied design tokens and older uCode3/uCode4 dependency language;
- generated build/cache artifacts.

HomeNest appears materially closer to a working product than the legacy uCode2
prototype. Existing vertical slices are presumed worth preserving unless an
audit or clean build disproves them. The purpose of the future review is to
identify the strongest implementation path, consolidate duplicates, and
repair boundaries rather than restart the product.

This planning tidy-up does not compile, migrate, delete, or extend HomeNest
code.

## Locked boundary

HomeNest owns:

- household media catalogue and playback orchestration;
- TV/EPG/DVR product workflows;
- Home Assistant/Matter-facing household integration;
- controller-first, television, kiosk, and appliance UX;
- Linux household deployment and service health;
- household-specific storage and policy.

HomeNest does not own:

- GridCore or lattice algebra;
- BBCSDL/AMOS runtime execution;
- uCode Runtime Capsules, LENS, or SKIN contracts;
- uCode 2 spatial lifting or Minecraft export;
- the canonical uCore MCP gateway or general workflow orchestration.

## Future consolidation sequence

This work is explicitly outside the active uCode sprints.

1. Inventory docs and code by capability and ownership.
2. Choose one server, one console application, one installer path, and one
   package layout.
3. Prove current vertical slices with builds and tests, then record modules as
   canonical, candidates, prototypes, or stale.
4. Define storage, network, identity, and external-service boundaries.
5. Consolidate around the strongest current scaffold; create a replacement
   scaffold only if no existing path passes the product checks.
6. Verify media discovery -> title detail -> playback -> now playing first.
7. Add TV/DVR and home automation only after the core path is reliable.
8. Compile, test, package, and deploy on a clean supported Linux target.

## Useful concepts to preserve

- Jellyfin as an optional media backend rather than hidden product ownership;
- controller-first spatial focus and ten-foot UI;
- household-safe offline behavior;
- clear client capability contracts;
- media-vault indexing and playback state;
- appliance health, install, rollback, and recovery;
- soft integration with uCore rather than a hard application dependency.

## Drift guards

Active HomeNest docs must not describe it as uCode3, depend on uCode4, claim
that uCode2 owns media services, or copy uCode runtime responsibilities into
the household server. Hard-coded household paths must be treated as deployment
profiles, not universal architecture.
