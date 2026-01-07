import { usersReadUserMe } from '~/generated/api';
import type { UserPublic } from '~/generated/api';

export const useAuth = () => {
    const user = useState<UserPublic | null>('user', () => null);
    const token = useCookie('access_token');

    async function loadUser() {
        if (!token.value) {
            user.value = null;
            return null;
        }

        const res = await usersReadUserMe({});

        if (res.data) {
            user.value = res.data;
            return user.value;
        } else {
            user.value = null;
            return null;
        }
    }

    function logout() {
        token.value = null;
        user.value = null;
    }

    return { user, loadUser, logout };
};
