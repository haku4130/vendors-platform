import type { RequirementItem, ServicePublicShort } from '~/generated/api';

export type { RequirementItem as Requirement };

export interface AnswersType {
    projectName: string;
    servicesNeeded: ServicePublicShort[];
    startTime: string;
    budget: number;
    locationPreference: string;
    exactLocation: string | null;
    website: string | null;
    projectIntroduction: string;
    questions: string[];
    requirements: RequirementItem[];
}
