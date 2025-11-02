export interface AnswersType {
    projectDescription: string;
    companyType: string;
    startTime: string;
    locationPreference: string;
    website: string;
    noWebsite: boolean;
    companyInfo: {
        companyName: string;
        companyAbout: string;
    };
}
