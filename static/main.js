const UPDATE_INTERVAL = 3*1000 // 3 seconds

let V = new Vue({
    el: '#app',
    data: {
        // API data
        data: undefined,
        ip: "mc.mmolo.co"
    },
    methods: {
        getData: async function() {
            // Using jsonp cors proxy for kraken api
            let response = await axios.get('/query')

            this.data = response.data

            // Recall the function to update data again
            setTimeout(this.getData, UPDATE_INTERVAL)
        }
    },
    filters: {
        head: function(player) {
            return "https://minotar.net/helm/"+player+"/50.png"
        }
    },
    created: function() {
        this.getData()
    }
})
