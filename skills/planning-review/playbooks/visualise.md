<!-- planning:guidance -->
# When a finding needs a picture

A finding a reader has to reassemble in their head is a finding that gets
skimmed, and a skimmed report did not happen. A diagram is not decoration here
— it is the finding, in the form that costs the reader least.

It is also not free. A picture that restates a sentence costs the reader twice:
once to read the sentence, once to check the picture says the same thing.

## The four triggers

A diagram is owed when **any one** of these holds. None of them is "it would
look nice".

| Trigger | Holds when | Because |
|---|---|---|
| `hops` | The finding spans three or more places the reader must hold at once | Prose makes them remember; a picture makes them look |
| `ordering` | It depends on sequence — the same parts in another order would be fine | "Then... then... then" in the prose is the tell |
| `disagreement` | Two things state different values and both must be shown to see it | Two paragraphs make the reader diff them by eye |
| `location` | It is somewhere in a two-dimensional artifact — a region, a crop, a layout | Words for a position are longer and less exact than a mark |

In this family `ordering` and `hops` fire most: a plan is a graph, and almost
every readiness finding is about a path through it. `location` fires as a
coverage grid — what the plan names against what it never mentions, which is
the shape a silence audit already has.

## When not to

- One place, one line, one sentence. Say it
- The picture would contain exactly what the sentence contains
- Nothing was traced. A diagram of an untraced path is speculation with better
  graphics, and the finding is not at its floor either
- The diagram would need the whole artifact to make sense. Bound it or drop it

## Which form

**ASCII by default.** It survives a terminal, a plain-text report, a commit
message and a diff, and it cannot fail to render. Every trigger above has an
ASCII form in [diagram-forms](../reference/diagram-forms.md).

**Mermaid when the shape is genuinely a graph** — more than about six nodes, or
branching and merging that ASCII would misalign. It needs a renderer, so it is a
trade, not an upgrade.

**Never both for one finding.** Two pictures of one thing is the reader
checking them against each other.

## The floor

A diagram carries the same evidence tag as the finding it belongs to. It never raises
one, and three things keep it a finding rather than an illustration:

- **`labelled`** — every mark names something that was opened. A region, a file,
  a step that exists. An unlabelled box is a guess that looks like a fact
- **`derived`** — it says nothing the evidence did not establish. It adds no hop
  nobody traced and no cause nobody checked
- **`bounded`** — it shows the parts the finding is about and stops. A diagram
  of the whole thing is a second thing to read

**The test:** could a reader who disagrees point at the part of the diagram that
is wrong, and check it? If not, it is not carrying a finding.

## Where it goes

Inside the finding, under the row it belongs to — not in a gallery at the end.
A picture separated from its claim is a puzzle.

One finding, one diagram. Where several findings share a location, one map with
numbered marks and the findings referring to the numbers beats one map each.

## In this family

- **A dependency graph** for anything with `hops` or `ordering` — tasks as
  nodes, the critical path marked, and the finding hung off the edge it is
  about. Mermaid earns its keep here more than anywhere else in the family
- **A coverage grid** for a silence audit: what a plan has to settle down one
  axis, what this plan settles across the other, and the blank row as the
  finding. The absence is the point, and a blank cell shows it faster than a
  paragraph saying nothing was said
- **A timeline** when the finding is that two pieces of work were sequenced as
  though independent — two lanes, the shared resource marked where they collide
- **Two columns** when an estimate and a constraint disagree: the range against
  the date, on one line
