export default defineAppConfig({
    ui: {
        button: {
            defaultVariants: {
                variant: 'outline',
            },
            compoundVariants: [
                {
                    color: 'primary',
                    variant: 'outline',
                    class: 'hover:bg-primary hover:text-white active:bg-primary/75 active:text-white',
                },
                {
                    color: 'primary',
                    variant: 'solid',
                    class: 'border hover:bg-white hover:text-black active:bg-primary/10 active:text-black disabled:hover:text-white',
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
