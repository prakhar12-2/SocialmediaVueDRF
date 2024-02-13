<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
                    <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                        <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full">
                        
                        <p><strong>{{ user.name }}</strong></p>

                        <div class="mt-6 flex space-x-8 justify-around">
                            <RouterLink :to="{name:'friends' ,params:{id:user.id}}" class="text-xs text-gray-500">{{ user.friends_count }} friends</RouterLink>
                            <p class="text-xs text-gray-500">120 posts</p>
                        </div>
                        <div class="mt-6">
                            <button v-if="userStore.user.id!=user.id" class="inline-vlock py-4 px-6 bg-red-600 text-sm text-white rounded-lg" @click="SendRequest">Request</button>
                            
                            <button  v-if="userStore.user.id == user.id" class="inline-block py-4 px-6 bg-emerald-600 text-sm text-white rounded-lg" @click="Logout">Logout</button>
                        </div>
                    </div>
        </div>
        <div class="main-center col-span-2 space-y-4">
                    <div 
                    class="bg-white border border-gray-200 rounded-lg"
                    v-if="userStore.user.id === user.id">
                    <form   v-on:submit.prevent="submitFirm" method="post">
                        <div class="p-4"> 
                            <textarea v-model="body" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What are you thinking about?"></textarea>
                        </div>

                        <div class="p-4 border-t border-gray-100 flex justify-between">
                            <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

                            <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
                        </div>
                    </form>
                    </div>

                    <div class="p-4 bg-white border border-gray-200 rounded-lg"
                         v-for="post in posts"
                         v-bind:key="post.id">
                         <FeedItem v-bind:post="post"/>
                    </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
         <youmknow/>
         <Trends/>
        </div>
    </div>
</template>
<script>
import youmknow from '@/components/youmknow.vue';
import Trends from '@/components/Trends.vue';
import axios from 'axios';
import { useUserStore } from '@/stores/user'
import FeedItem from '@/components/FeedItem.vue';
import { RouterLink } from 'vue-router';
import { useToastStore } from '@/stores/toast';
export default{
    name:'FeedView',
    setup() {
        const userStore = useUserStore()
        const toastStore =useToastStore()
        return {
            userStore,
            toastStore
        }
    },
    components:{
    youmknow,
    Trends,
    FeedItem,
    RouterLink
},
    data(){
        return{
            posts:[],
            user:{
                id:null
            },
            body:'',
        }
    },
    mounted(){
        this.getfeed()
    },
    watch:{
        '$route.params.id':{
            handler:function(){
                this.getfeed()
            },
            deep:true,
            immediate:true
        }
    }
    ,
    methods:{
        SendRequest(){
            axios
            .post(`api/friends/request/${this.$route.params.id}/`)
            .then(response=>{
                console.log('data',response)
                if(response.data.message=='Request Sent successfully'){
                    this.toatstStore.showToast(5000, 'Request Sent Successfully', 'bg-emerald-500')
                }
                else{
                    this.toastStore.showToast(5000, 'Request has been sent already', 'bg-red-300')
                }
            })
            .catch(error=>{
                console.log('error:',error)
            })
        },
        getfeed(){
            axios
            .get(`/api/post/profile/${this.$route.params.id}/`)
            .then(response=>{
                console.log('data',response)
                this.posts=response.data.posts
                this.user=response.data.user
            })
            .catch(error=>{
                console.log('error',error)
            })
        },
        submitFirm(){
            console.log('submitFirm',this.body)
            axios
            .post('/api/post/create/',{
                'body':this.body
            },{
                headers: {
                    'Content-Type': 'application/json',
                 }
                }
            )
            .then(response=>{
                console.log('data',response.data)
                this.posts.unshift(response.data)
            })
            .catch(error=>{
                console.log('error',error)
            })
        },
        Logout(){
            this.userStore.removeToken()
            this.$router.push('/login')
            

        }

        
    }
}
</script>