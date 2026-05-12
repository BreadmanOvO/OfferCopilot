export type IntentFormDraft = {
  cities: string[];
  technicalField: string;
  customField: string;
  targetRoles: string[];
  companyTypes: string[];
};

export const INITIAL_INTENT_FORM_DRAFT: IntentFormDraft = {
  cities: [],
  technicalField: "",
  customField: "",
  targetRoles: [],
  companyTypes: [],
};

function areStringArraysEqual(left: string[], right: string[]) {
  return (
    left.length === right.length &&
    left.every((value, index) => value === right[index])
  );
}

export function areIntentFormDraftsEqual(
  left: IntentFormDraft,
  right: IntentFormDraft
) {
  return (
    areStringArraysEqual(left.cities, right.cities) &&
    left.technicalField === right.technicalField &&
    left.customField === right.customField &&
    areStringArraysEqual(left.targetRoles, right.targetRoles) &&
    areStringArraysEqual(left.companyTypes, right.companyTypes)
  );
}

export function normalizeIntentFormDraft(
  draft?: Partial<IntentFormDraft>
): IntentFormDraft {
  return {
    cities: draft?.cities ?? INITIAL_INTENT_FORM_DRAFT.cities,
    technicalField:
      draft?.technicalField ?? INITIAL_INTENT_FORM_DRAFT.technicalField,
    customField: draft?.customField ?? INITIAL_INTENT_FORM_DRAFT.customField,
    targetRoles: draft?.targetRoles ?? INITIAL_INTENT_FORM_DRAFT.targetRoles,
    companyTypes: draft?.companyTypes ?? INITIAL_INTENT_FORM_DRAFT.companyTypes,
  };
}

export function syncIntentFormDraft(
  currentDraft: IntentFormDraft,
  incomingDraft?: Partial<IntentFormDraft>
) {
  const nextDraft = normalizeIntentFormDraft(incomingDraft);
  return areIntentFormDraftsEqual(currentDraft, nextDraft)
    ? currentDraft
    : nextDraft;
}
