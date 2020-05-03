export const userStore = {
    state: {
        login: false,
        uid: '',
        username: ''
    },
    getters: {
        user(state) {
            return {
                uid: state.uid,
                username: state.username
            };
        }
    },
    mutations: {
        login(state, data) {
            console.log('in login, data:', data);
            state.login = true;
            state.username = data.username;
            state.uid = data.uid;
            uni.setStorage({
                key: 'user',
                data: {
                    uid: state.uid,
                    username: state.username
                }
            });
        },
        logout(state) {
            state.login = false;
            state.username = null;
            state.uid = null;
            uni.removeStorage({ key: 'user' });
        },
        setUser(state, user) {
            if (
                user !== undefined &&
                user.uid !== undefined &&
                user.username !== undefined
            ) {
                state.login = true;
                state.uid = user.uid;
                state.username = user.username;
            }
        }
    }
};
