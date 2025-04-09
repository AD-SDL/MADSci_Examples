# MADSci Examples

```mermaid
stateDiagram
  direction LR
  [*] --> Queued:Workflow Submitted
  Queued --> Running:Started First Step
  Queued --> Failed:Problem starting First Step
  Running --> InProgress:Succeeded Non-Terminal Step
  InProgress --> Running:Started Next Step
  Queued --> Cancelled:Cancelled by User
  Running --> Cancelled:Cancelled by User
  Running --> Completed:Succeeded Final Step
  Paused --> Running:Resumed by User
  Running --> Paused:Paused by User
  InProgress --> Paused:Paused by User
  InProgress --> Cancelled:Cancelled by User
  Failed --> InProgress:Retrying Step
  Failed --> Queued:Resubmitted by User
  Cancelled --> InProgress:Retrying Step
  Cancelled --> Queued:Resubmitted by User
  Completed --> Queued:Resubmitted by User
  Queued --> Paused:Paused by User
  Paused --> Queued:Resumed by User

  Queued:queued
  Running:running
  Failed:failed
  InProgress:in_progress
  Cancelled:cancelled
  Completed:completed
  Paused:paused

```


## Generating Mermaid Diagrams

Use https://github.com/mermaid-js/mermaid-cli
