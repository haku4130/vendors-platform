import type { ServicePublicShort } from '~/generated/api';

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
    requirements: string[];
}
