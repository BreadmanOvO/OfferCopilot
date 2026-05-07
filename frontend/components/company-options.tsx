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
      <h2>推荐公司</h2>
      <ul>
        {options.map((option) => (
          <li key={option.company_name}>
            <strong>{option.company_name}</strong>
            <p>{option.reason}</p>
            <button type="button" onClick={() => onSelect(option.company_name)}>选择这家公司</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
