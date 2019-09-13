<template>
    <v-app>
    <CalendarEvent />
    </v-app>
</template>

<script>
import CalendarEvent from './components/CalendarEvent'

export default {
  name: 'App',
  components: {
    CalendarEvent
  },
  data () {
    return {
      //
    }
  }
}
</script>
