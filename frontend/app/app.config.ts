export default defineAppConfig({
    ui: {
        colors: {
            primary: 'blue',
            secondary: 'sky',
        },
        button: {
            defaultVariants: {
                variant: 'outline',
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: 'outline',
                    class: 'hover:bg-primary hover:text-white disabled:text-black active:bg-primary/75 active:text-white',
                },
                {
                    color: 'primary',
                    variant: 'solid',
                    class: 'hover:bg-blue-700 active:bg-blue-800',
                },
                {
                    color: 'warning',
                    variant: 'solid',
                    class: 'bg-[#8B2E2E] hover:bg-[#A63B3B] active:bg-red-900/70 disabled:bg-bg-[#8B2E2E] text-white',
                },
            ],
        },
        radioGroup: {
            compoundVariants: [
                {
                    color: 'primary',
                    variant: 'card',
                    class: {
                        item: 'hover:bg-primary/5 active:bg-primary/10 transition',
                    },
                },
            ],
        },
        formField: {
            slots: {
                error: 'text-start',
            },
        },
        input: {
            slots: {
                trailingIcon: 'text-muted',
                leadingIcon: 'text-muted',
            },
        },
        inputMenu: {
            slots: {
                tagsInput: 'placeholder:text-normal',
            },
            variants: {
                multiple: {
                    false: {
                        base: 'placeholder:text-normal',
                    },
                },
            },
        },
    },
});
