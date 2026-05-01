# OfferCopilot Local Instructions

- When the working directory is `/root/workspace/OfferCopilot`, write all Claude-generated project documents to `/root/workspace/OfferCopilot/OfferCopilotDocs/`.
- Treat specs, plans, design docs, analysis docs, architecture notes, and generated README content as documentation that belongs in `OfferCopilotDocs`.
- Do not create project documentation files in the main repository unless the user explicitly asks for a file to live there.
- Treat `.claude/` and `.omc/` as local runtime directories. Leave them local and never commit them.
