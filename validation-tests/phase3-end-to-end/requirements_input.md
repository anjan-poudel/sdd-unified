# SDD Use Case: Finite-State-Machine Workflow Engine with Parallel Processing

## Feature Overview

**Goal:** Develop a Java library for a finite-state-machine engine that supports parallel processing and transition tracking for complex business workflows.

**Business Context:** Order fulfillment systems, document approval workflows, manufacturing processes, and other business operations that require:
- Sequential and parallel task execution
- State transition validation
- Event-driven status updates
- Audit trails for compliance

## High-Level Architecture

### Core Components

```
Workflow<T>
  └─ List<WorkflowItemGroup>
       └─ List<WorkflowItem<T>>
```

### State Transition Model

```
Business Object States:
RECEIVED → PREPARING → PACKING → DELIVERING → COMPLETED
                ↓
            CANCELLED (terminal state)

Invalid Transitions:
CANCELLED → DELIVERING (rejected)
COMPLETED → PREPARING (rejected)
```

## Detailed Requirements

### 1. Core Classes

#### Workflow<T>
```java
public class Workflow<T> {
    private String name;
    private String workflowId;
    private List<WorkflowItemGroup<T>> groups;
    private WorkflowState state;
    private TransitionMap transitionMap;
    private WorkflowEventPublisher eventPublisher;

    // Executes all groups in sequence, returns final result
    public T execute();

    // Validates if workflow can transition to target state
    public boolean canTransition(WorkflowState from, WorkflowState to);

    // Returns current aggregated state
    public WorkflowState getCurrentState();
}
```

**Requirements:**
- FR-001: Workflow must track execution across all groups
- FR-002: Workflow must publish events at start, completion, and state transitions
- FR-003: Workflow must validate state transitions using TransitionMap
- FR-004: Workflow must aggregate final state from all group executions

#### WorkflowItemGroup<T>
```java
public class WorkflowItemGroup<T> {
    private String name;
    private List<WorkflowItem<T>> items;
    private WorkflowState status;
    private boolean parallel;
    private ExecutorService executorService;
    private CountDownLatch completionLatch;

    // Executes items (parallel or sequential based on flag)
    public List<T> execute();

    // Waits for all parallel items to complete
    public void awaitCompletion(long timeout, TimeUnit unit);

    // Calculates group status from item statuses
    public WorkflowState calculateGroupStatus();
}
```

**Requirements:**
- FR-005: Group must support both sequential and parallel execution modes
- FR-006: Parallel groups must collect all item statuses before calculating final group status
- FR-007: Group must handle out-of-order status updates in parallel mode
- FR-008: All items in a parallel group must agree on next transition state
- FR-009: Group must publish events when status changes

#### WorkflowItem<T>
```java
public interface WorkflowItem<T> {
    T execute() throws WorkflowExecutionException;
    WorkflowState getStatus();
    void setStatus(WorkflowState status);
    String getItemId();
    WorkflowState getNextTransitionState();
}
```

**Requirements:**
- FR-010: Items must be independently executable
- FR-011: Items must track their own status
- FR-012: Items must declare their expected next transition state
- FR-013: Items must handle execution failures gracefully

### 2. State Transition Management

#### TransitionMap
```java
public class TransitionMap {
    private Map<WorkflowState, Set<WorkflowState>> validTransitions;
    private Map<WorkflowState, Set<WorkflowState>> parallelGroupTransitions;

    // Validates if transition is allowed
    public boolean isValidTransition(WorkflowState from, WorkflowState to);

    // Validates parallel group transitions
    public boolean validateParallelGroupTransitions(
        List<WorkflowState> itemStates,
        WorkflowState targetState
    );

    // Returns all valid next states from current state
    public Set<WorkflowState> getValidNextStates(WorkflowState current);
}
```

**Requirements:**
- FR-014: Must define valid state transitions for business objects
- FR-015: Must prevent invalid transitions (e.g., CANCELLED → DELIVERING)
- FR-016: Must support parallel group transition validation
- FR-017: Must validate that all items in parallel group target same next state

**Example Transition Rules:**
```
RECEIVED → {PREPARING, CANCELLED}
PREPARING → {PACKING, CANCELLED}
PACKING → {DELIVERING, CANCELLED}
DELIVERING → {COMPLETED, CANCELLED}
CANCELLED → {} (terminal)
COMPLETED → {} (terminal)
```

### 3. Event Publishing System

#### WorkflowEventPublisher
```java
public interface WorkflowEventPublisher {
    void publishWorkflowStarted(WorkflowEvent event);
    void publishWorkflowCompleted(WorkflowEvent event);
    void publishStateTransition(StateTransitionEvent event);
    void publishGroupStarted(GroupEvent event);
    void publishGroupCompleted(GroupEvent event);
    void publishItemCompleted(ItemEvent event);
}

public class WorkflowEvent {
    private String workflowId;
    private String workflowName;
    private WorkflowState state;
    private Instant timestamp;
    private Map<String, Object> metadata;
}

public class StateTransitionEvent extends WorkflowEvent {
    private WorkflowState fromState;
    private WorkflowState toState;
    private String triggeredBy; // item or group ID
}
```

**Requirements:**
- FR-018: Publish events at workflow level (start, complete, state change)
- FR-019: Publish events at group level (start, complete, status change)
- FR-020: Publish events at item level (complete, status change)
- FR-021: Events must include timestamps and contextual metadata
- FR-022: Event publishing must not block workflow execution

### 4. Parallel Processing Semantics

**Requirements:**
- FR-023: Parallel groups must execute items concurrently using thread pools
- FR-024: Parallel execution must collect all results before proceeding
- FR-025: If ANY item in parallel group fails, group status calculation must account for it
- FR-026: Status updates can arrive out-of-order; final status only after all items report
- FR-027: All items in parallel group must have same `getNextTransitionState()` value
- FR-028: Group state calculation must validate transition consistency

**Parallel Status Aggregation Algorithm:**
```
Given: Parallel group with items [I1, I2, I3]
  I1 completes at T1 with status PREPARING
  I3 completes at T2 with status PREPARING (out of order)
  I2 completes at T3 with status PREPARING

At T1: Group waits (1/3 complete)
At T2: Group waits (2/3 complete)
At T3: Group validates:
  - All items complete? YES
  - All same next state? YES (all → PREPARING)
  - Valid transition from current? YES
  → Group transitions to PREPARING
  → Publish GroupCompletedEvent
```

### 5. Concrete Example: Order Fulfillment Workflow

```java
// Business object
public class Order {
    private String orderId;
    private OrderState state;
    private List<OrderLine> items;
    private PaymentInfo payment;
}

// Workflow definition
Workflow<Order> orderWorkflow = new Workflow.Builder<Order>()
    .name("order-fulfillment")
    .transitionMap(OrderTransitionMap.standard())
    .eventPublisher(new KafkaEventPublisher())
    .addGroup(
        new WorkflowItemGroup.Builder<Order>()
            .name("validation-checks")
            .parallel(true) // Run validations concurrently
            .addItem(new InventoryCheckItem())
            .addItem(new PaymentValidationItem())
            .addItem(new AddressVerificationItem())
            .build()
    )
    .addGroup(
        new WorkflowItemGroup.Builder<Order>()
            .name("preparation")
            .parallel(false) // Sequential
            .addItem(new ReserveInventoryItem())
            .addItem(new GeneratePickListItem())
            .build()
    )
    .addGroup(
        new WorkflowItemGroup.Builder<Order>()
            .name("fulfillment")
            .parallel(true) // Pack and label concurrently
            .addItem(new PackOrderItem())
            .addItem(new PrintShippingLabelItem())
            .build()
    )
    .build();

// Execute
Order result = orderWorkflow.execute();
```

**State Flow:**
```
Order received: state = RECEIVED
↓
validation-checks (parallel):
  InventoryCheckItem → validates → next state = PREPARING
  PaymentValidationItem → validates → next state = PREPARING
  AddressVerificationItem → validates → next state = PREPARING
  → All complete, all agree on PREPARING
  → Order transitions: RECEIVED → PREPARING
  → Event published: StateTransitionEvent(RECEIVED → PREPARING)
↓
preparation (sequential):
  ReserveInventoryItem → executes → next state = PACKING
  GeneratePickListItem → executes → next state = PACKING
  → Order transitions: PREPARING → PACKING
↓
fulfillment (parallel):
  PackOrderItem → executes → next state = DELIVERING
  PrintShippingLabelItem → executes → next state = DELIVERING
  → All complete, all agree on DELIVERING
  → Order transitions: PACKING → DELIVERING
  → Event published: StateTransitionEvent(PACKING → DELIVERING)
```

### 6. Error Handling and Cancellation

**Requirements:**
- FR-029: If item execution throws exception, mark item as FAILED
- FR-030: Failed items in sequential group stop group execution immediately
- FR-031: Failed items in parallel group allow others to complete, then aggregate status
- FR-032: Workflow must support cancellation at any point
- FR-033: CANCELLED is a terminal state; no transitions out of CANCELLED
- FR-034: Cancelled workflow must publish cancellation event

**Cancellation Scenario:**
```java
Order order = ...; // state = PREPARING

// External cancellation request
orderWorkflow.cancel();

Current behavior:
- If in sequential group, current item completes, no further items execute
- If in parallel group, items in flight complete, new items not started
- Order transitions: PREPARING → CANCELLED
- Event published: StateTransitionEvent(PREPARING → CANCELLED, reason=USER_CANCELLED)
- Subsequent groups not executed
```

### 7. Non-Functional Requirements

**NFR-001: Performance**
- Parallel groups must execute items concurrently with configurable thread pool
- Target: Process workflows with 50 items in < 5 seconds (excluding item logic)

**NFR-002: Thread Safety**
- All state transitions must be thread-safe
- Status aggregation in parallel groups must use proper synchronization

**NFR-003: Observability**
- All state transitions must be logged
- Event publishing must succeed within 100ms
- Metrics: workflow duration, group duration, item duration

**NFR-004: Extensibility**
- WorkflowItem interface allows custom implementations
- TransitionMap can be customized per business domain
- Event publishers can be swapped (Kafka, RabbitMQ, in-memory)

**NFR-005: Testability**
- Framework must support unit testing of individual items
- Mock event publishers for testing
- Synchronous execution mode for deterministic testing

## Acceptance Criteria (BDD Format)

### Scenario 1: Sequential Group Execution
```gherkin
Given a workflow with a sequential group containing 3 items
When the workflow is executed
Then items execute in order: item1, then item2, then item3
And each item completes before the next starts
And group status updates after each item
```

### Scenario 2: Parallel Group Execution
```gherkin
Given a workflow with a parallel group containing 3 items
When the workflow is executed
Then all 3 items execute concurrently
And group waits for all items to complete
And group status is calculated only after all items report
```

### Scenario 3: Valid State Transition
```gherkin
Given an order in RECEIVED state
And a workflow item that sets next state to PREPARING
When the item executes successfully
Then the order transitions from RECEIVED to PREPARING
And a StateTransitionEvent is published
```

### Scenario 4: Invalid State Transition Blocked
```gherkin
Given an order in CANCELLED state
And a workflow item that attempts to set next state to DELIVERING
When the transition is validated
Then the transition is rejected as invalid
And an exception is thrown
```

### Scenario 5: Parallel Group State Consensus
```gherkin
Given a parallel group with 3 items
And all items declare next state as PREPARING
When all items complete
Then the group validates state consensus
And the workflow transitions to PREPARING
```

### Scenario 6: Parallel Group State Mismatch
```gherkin
Given a parallel group with 3 items
And item1 declares next state as PREPARING
And item2 declares next state as CANCELLED
When all items complete
Then the group detects state mismatch
And throws StateConsensusException
```

### Scenario 7: Out-of-Order Status Updates
```gherkin
Given a parallel group with items [A, B, C]
When item C completes first at T1
And item A completes second at T2
And item B completes last at T3
Then group waits until T3 for all completions
And calculates final status at T3
And publishes GroupCompletedEvent at T3
```

### Scenario 8: Workflow Cancellation
```gherkin
Given a workflow in PREPARING state
When cancel() is called
Then the workflow transitions to CANCELLED state
And a StateTransitionEvent(PREPARING → CANCELLED) is published
And subsequent groups are not executed
And no further state transitions are possible
```

### Scenario 9: Item Failure in Sequential Group
```gherkin
Given a sequential group with items [A, B, C]
And item B throws an exception
When the group executes
Then item A completes successfully
And item B fails with exception
And item C is not executed
And group status is set to FAILED
```

### Scenario 10: Event Publishing for Full Workflow
```gherkin
Given a workflow with 2 groups and 5 total items
When the workflow executes end-to-end
Then WorkflowStartedEvent is published at start
And GroupStartedEvent is published for each group
And ItemCompletedEvent is published for each item (5 events)
And StateTransitionEvent is published at each state change
And GroupCompletedEvent is published for each group
And WorkflowCompletedEvent is published at end
```

## Design Considerations

### 1. Thread Pool Management
- Use configurable `ExecutorService` per WorkflowItemGroup
- Default: `ForkJoinPool.commonPool()`
- Allow custom executors for isolation (e.g., critical workflows)

### 2. State Aggregation Logic
```java
// In WorkflowItemGroup.calculateGroupStatus()
if (parallel) {
    // Wait for all items
    completionLatch.await(timeout, TimeUnit.SECONDS);

    // Collect all item next states
    Set<WorkflowState> nextStates = items.stream()
        .map(WorkflowItem::getNextTransitionState)
        .collect(Collectors.toSet());

    // Validate consensus
    if (nextStates.size() != 1) {
        throw new StateConsensusException(
            "Parallel group items disagree on next state: " + nextStates
        );
    }

    WorkflowState targetState = nextStates.iterator().next();

    // Validate transition
    if (!transitionMap.isValidTransition(currentState, targetState)) {
        throw new InvalidTransitionException(
            currentState + " → " + targetState
        );
    }

    return targetState;
}
```

### 3. Event Schema Design
```json
{
  "eventType": "STATE_TRANSITION",
  "workflowId": "WF-12345",
  "workflowName": "order-fulfillment",
  "timestamp": "2025-10-16T19:30:00Z",
  "fromState": "PREPARING",
  "toState": "PACKING",
  "triggeredBy": "group-preparation",
  "metadata": {
    "orderId": "ORD-98765",
    "itemCount": 3,
    "totalValue": 149.99
  }
}
```

### 4. Testing Strategy
- **Unit Tests:** Test individual items in isolation
- **Integration Tests:** Test groups with mock items
- **End-to-End Tests:** Full workflows with real state transitions
- **Concurrency Tests:** Validate thread safety with parallel execution
- **Chaos Tests:** Random failures, cancellations, timeouts

## Implementation Plan Outline

### Phase 1: Core State Machine (L3 Tasks 1-5)
1. Implement `WorkflowState` enum and `TransitionMap` class
2. Create `WorkflowItem` interface and abstract base class
3. Implement `WorkflowItemGroup` with sequential execution
4. Implement `Workflow` class with basic execution
5. Add state transition validation

### Phase 2: Parallel Processing (L3 Tasks 6-10)
6. Add parallel execution support to `WorkflowItemGroup`
7. Implement `CountDownLatch` for parallel completion tracking
8. Create status aggregation algorithm for parallel groups
9. Add state consensus validation
10. Handle out-of-order completion scenarios

### Phase 3: Event System (L3 Tasks 11-15)
11. Define event interfaces and data classes
12. Implement `WorkflowEventPublisher` interface
13. Create in-memory event publisher for testing
14. Integrate event publishing into workflow execution
15. Add async event publishing with executor

### Phase 4: Error Handling (L3 Tasks 16-20)
16. Add exception handling to item execution
17. Implement cancellation support
18. Add timeout handling for parallel groups
19. Create error recovery strategies
20. Implement circuit breaker for failing items

### Phase 5: Production Readiness (L3 Tasks 21-25)
21. Add comprehensive logging
22. Implement metrics collection
23. Create builder pattern for workflow construction
24. Add workflow persistence (optional)
25. Write documentation and examples

## Success Metrics

- ✅ All 34 functional requirements implemented
- ✅ All 5 non-functional requirements met
- ✅ All 10 BDD scenarios passing
- ✅ Code coverage > 85%
- ✅ Zero concurrency bugs in parallel execution
- ✅ Performance target met (50 items in < 5s)

## SDD Framework Integration

This use case is ideal for the SDD Unified Framework because:

1. **Clear Requirements:** Well-defined state machine semantics
2. **Layered Design:** L1 (architecture), L2 (component APIs), L3 (implementation tasks)
3. **Testable Criteria:** BDD scenarios provide clear acceptance criteria
4. **Multiple Agents:** BA defines requirements, Architect designs state machine, PE designs APIs, LE creates tasks, Coder implements
5. **Review Cycles:** Complex concurrency logic benefits from multi-agent review

### Recommended Workflow

```bash
# In Claude Code with SDD Unified installed
/feature "Finite-state-machine workflow engine with parallel processing support for Java. See requirements in use_cases/FSM_PARALLEL_WORKFLOW_ENGINE.md"

# Framework will:
# 1. sdd-ba creates formal spec.yaml from this document
# 2. sdd-architect designs L1 architecture (state machine design, concurrency model)
# 3. sdd-pe designs L2 components (detailed class APIs, thread pool strategy)
# 4. sdd-le creates L3 tasks (25 tasks as outlined above)
# 5. sdd-coder implements each task with BDD validation
```

## Related Patterns and Technologies

- **State Pattern:** Core design pattern for state machine
- **Strategy Pattern:** For custom WorkflowItem implementations
- **Template Method:** For AbstractWorkflowItem base class
- **Observer Pattern:** For event publishing
- **Fork-Join Framework:** For parallel execution
- **CompletableFuture:** For async operations
- **Spring State Machine:** Similar existing framework (reference)
- **Apache Camel:** Workflow orchestration (reference)

---

**Document Version:** 1.0
**Created:** 2025-10-16
**For:** SDD Unified Framework v3
**Status:** Ready for `/feature` execution
