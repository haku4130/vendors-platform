export interface Step {
    key: string;
    title: string;
    placeholder?: string;
    required?: boolean;
    options?: string[];
    optionsColumns?: boolean;
    checkboxLabel?: string;
    fields?: Record<
        string,
        {
            label?: string;
            placeholder: string;
            required?: boolean;
        }
    >;
}
