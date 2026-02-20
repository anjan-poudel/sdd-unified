# alternative proposal

Instead of utilizing a full-fledged software team with PO,BA,PE,LE,Architect,Dev  etc, refactor the code to use pair programming and code review as the central 
and key strategies for agentic coding.

# how does it work?
either different models for different roles/responsibilities or well crafted system prompt or persona for different roles.

## Product session
- PO comes up with ideas for products etc
- BA reviews the ideas and provide feedback
- PO either incorporates the feedback or provide reasoning/rationale for his/her thinking.
- PO and BA work in pairs
- Once settled BA writes PRD and requirement documents ( assume all requisite cross team consultation and collaboration has occurred)
- PO takes backseat and lets BA drive the paired brainstorming session this time and he provides feedbacks.
- this iterates until PO is happy.
- Then the PRD becomes the project/feature primary requirements doc.

## Planning session
- Tasks coordinator - with help from BA, engineering manager,  Principal/Staff/Lead/Senior engineers to explore scope, feasibility, tradeoffs, justifications etc.
- PRD (Epic) gets broken into tasks (Stories) with detailed requirements, acceptance criteria ( gherkin tests).
   Optional technical details are added as needed to help explain complex issues with links to relevant resources. 
   This can include code fragments, designs, architecture existing/proposal - enough details for dev to be able to efficiently perform the taaks.

## Dev session
 - review PRD and Stories
- architecture and design - paired
- implementation and testing - paired
- release coordination of owned services and stack.

# post release
- deployment and post deloyment - paired
- support engineers - paired


# Core principle:
- each agent is paired with another agent ( different models as seen fit) for all tasks
- after each paired work, output/artifacts are formally reviewed by affected downstream teams - like PRD  ( or upstream if needed)
- Paired work to catch issues early and correct mistakes in early phase. and formal PR to catch issues not addressed by paired sessions 
- or issue too complex with cross-platform/team impacts, for devs working on it to fully realise the impact.

# planning sessions
- participants
--  BA/PE (product) 
--  LE/PE/Architect (engineering)
- stories are broken down into sub-tasks.
- technical details are added to subtask and story points.
- blockers raised/ plans for blockers resolutions prioritised.
- Story marked as `Ready for Dev` if all good.

# Quality gate
- paired session for product design ( 1sr Go/No-Go with pair input and discussions)
- Formal product design review.( 2nd Go/No-Go)
- paired dev sessions to catch issues early in SDLC ( 3rd Go/No-Go)
- code review to catch wider issues not considered by the pair or they lack subject matter expertise. ( 4th Go/No-Go)
- finally human in the loop if code reviewer doesn't have 90%+ confidence in its response or 90% or less ability to respond correctly.  ( 5th
- Go/No-Go)
