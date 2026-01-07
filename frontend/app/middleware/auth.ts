const auth_pages = ['/sign-in', '/register', '/password-reset', '/logout'];

export default defineNuxtRouteMiddleware(async (to, from) => {
    const auth = useAuth();

    if (auth.user.value) {
        if (
            auth.user.value.role === 'vendor' &&
            !auth.user.value.vendor_profile
        ) {
            if (
                to.path !== '/dashboard/vendor-registration' &&
                !auth_pages.includes(to.path)
            ) {
                const toast = useToast();
                toast.add({
                    title: 'Vendor profile required',
                    description: 'Please complete your vendor profile first',
                    color: 'error',
                });
                return navigateTo('/dashboard/vendor-registration');
            }
        }
        return;
    }

    if (await auth.loadUser()) return;

    const toast = useToast();
    toast.add({
        title: 'Authorization required',
        description: 'Please log in to access this page',
        color: 'error',
    });
    if (auth_pages.includes(from.path)) return abortNavigation();
    return navigateTo('/sign-in');
});
