import { getEvents } from '@/api/getEvents';

export const namespaced = true;

export const state = {
    events: []
};

export const mutations = {
    setEvents(state, data) {
        state.events = data
    }
};

export const actions = {
    async getAllEvents({commit}) {
        return commit('setEvents', await getEvents())
    }
}

export const getters = {

};
