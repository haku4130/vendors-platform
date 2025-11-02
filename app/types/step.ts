export interface Step {
    key: string;
    title: string;
    placeholder?: string;
    options?: string[];
    optionsColumns?: boolean;
    checkboxLabel?: string;
    fields?: Record<
        string,
        {
            label?: string;
            placeholder: string;
        }
    >;
}
