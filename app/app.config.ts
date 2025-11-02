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
                    class: 'border hover:bg-white hover:text-black active:bg-primary/10 active:text-black',
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
    },
});
