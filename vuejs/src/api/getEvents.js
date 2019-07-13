import axios from 'axios'

export function getEvents() {
    return axios.get('/api/event/')
        .then(res => {
            return res.data
        })
        .catch(err => {
            // eslint-disable-next-line
            console.error(err);
            throw err
        })
}
