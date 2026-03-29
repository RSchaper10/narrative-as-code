# Hosted Product Specification

## Purpose

This document describes the future hosted layer that sits on top of the local-first repository workflow. It is not implemented in this starter repo.

Treat this as product direction, not shipped functionality.

The hosted product should help authors and narrative teams work chapter by chapter while keeping the repository as the source of truth.

## Product Position

- local-first at the core
- hosted orchestration as an optional layer
- chapter-scoped workflows before full-manuscript automation
- human approval required before sync back to the repo

## Core Chapter Flow

1. Import or upload a chapter from the repository or from a draft buffer.
2. Pull grounding context from canon, metadata, research, and strategy notes.
3. Trigger a workflow run against the selected chapter.
4. Present outputs for review in distinct action modes.
5. Let the user accept, reject, regenerate, or refine results.
6. Update metadata and metrics if accepted changes alter project state.
7. Sync approved changes back to the repository.
8. Rebuild downstream artifacts on demand.

## Entity Definitions

### `Project`

- identity for one manuscript system
- points to repo configuration and default workflow policies
- owns chapters, canon documents, research packets, strategy notes, and artifacts

### `Chapter`

- one narrative unit under active revision
- includes manuscript content plus metadata such as order, title, POV, status, and summary
- supports multiple workflow runs over time

### `CanonDocument`

- durable truth or controlled ambiguity document
- includes story bible, character notes, location rules, continuity bridges, and open questions

### `ResearchPacket`

- concise source-backed support document scoped to a topic, setting, technology, or craft need
- intended for scene use, not generic hoarding

### `StrategyNote`

- planning document that guides revision priorities, publishing steps, editorial constraints, or workflow rules

### `WorkflowRun`

- one recorded execution of an action against a chapter or project
- stores prompt context, inputs, outputs, timestamps, status, and reviewer decision

### `Artifact`

- generated output such as compiled manuscript, chapter analysis, stats JSON, EPUB, DOCX, synopsis draft, or review report

## Supported Workflow Actions

### `generate`

- create new prose or support material from a defined scaffold

### `extend`

- continue or deepen existing chapter material without replacing approved text wholesale

### `refine`

- improve clarity, pacing, tension, structure, or style against explicit constraints

### `review`

- inspect for continuity, logic, pacing, tone, or readiness issues without rewriting by default

### `edit`

- apply targeted text changes to approved content with clear diffs

### `analyze`

- calculate metrics, compare states, detect drift, and summarize project-level patterns

### `rebuild`

- regenerate compiled downstream artifacts after accepted changes

## Data Flow

- the repository remains the long-term source of truth
- the hosted layer reads from the repo or a synced project state
- runs operate on chapter-scoped working copies
- accepted outputs are converted into explicit file updates
- metadata and generated artifacts are refreshed after approval

## Acceptance Rules

- no silent overwrite of approved chapter text
- no canon changes without explicit human acceptance
- every workflow run must produce a diffable output
- project metrics must be recalculated after accepted text changes

## Recommended Early Interfaces

- chapter workbench with context panel
- run history with action labels
- diff review for prose and support files
- artifact viewer for compiled output and stats
- sync panel that shows pending repo changes
