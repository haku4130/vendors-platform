export default defineNuxtRouteMiddleware(() => {
    const auth = useAuth();

    if (!auth.user.value?.is_superuser) {
        return navigateTo(useLocalePath()('/dashboard'));
    }
});
