import { Source } from "../lib/types";

export function SourcesView({ sources }: { sources: Source[] }) {
  if (!sources.length) return null;

  return (
    <section>
      <h2>Sources ({sources.length})</h2>
      <ul>
        {sources.map((source) => (
          <li key={source.url}>
            <a href={source.url} target="_blank" rel="noopener noreferrer">
              {source.title || source.url}
            </a>
            {source.snippet ? <p>{source.snippet}</p> : null}
          </li>
        ))}
      </ul>
    </section>
  );
}
