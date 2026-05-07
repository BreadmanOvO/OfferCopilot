export function CompanyOptions({
  options,
  onSelect,
}: {
  options: Array<{ company_name: string; reason: string }>;
  onSelect: (companyName: string) => void;
}) {
  if (!options.length) return null;

  return (
    <section>
      <h2>Recommended Companies</h2>
      <ul>
        {options.map((option) => (
          <li key={option.company_name}>
            <strong>{option.company_name}</strong>
            <p>{option.reason}</p>
            <button type="button" onClick={() => onSelect(option.company_name)}>Continue with this company</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
