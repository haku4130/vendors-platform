export default defineNuxtRouteMiddleware(async () => {
    const auth = useAuth();

    if (auth.user.value?.role === 'vendor') return;

    return abortNavigation();
});
