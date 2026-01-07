export default defineNuxtRouteMiddleware(async () => {
    const auth = useAuth();

    if (auth.user.value?.role === 'company') return;

    return abortNavigation();
});
