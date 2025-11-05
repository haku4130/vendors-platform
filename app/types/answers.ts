export interface AnswersType {
    projectDescription: string;
    servicesNeeded: string[];
    startTime: string;
    locationPreference: string;
    website: string;
    noWebsite: boolean;
    companyInfo: {
        companyName: string;
        companyAbout: string;
    };
}
