import base from './index'
import Qs from 'qs'
let axios = base.axios
let baseUrl = base.baseUrl

//获取好友
// export const getFriend = params => {
//     return axios({
//       method: 'post',
//       baseURL: `${baseUrl}/friend/friendList`,
//       data: params
//     }).then(res => res.data)
//   }

export const getFriend = params => {
  return axios({
    method: 'get',
    baseURL: `${baseUrl}/chat/box/?ordering=-created_time/`,
    data: params
  }).then(res => res.data)
}


export const getChatMsg = params => {
  return axios({
    method: 'get',
    baseURL: `${baseUrl}/chat/${params.frinedId.replace(/-/g, "")}/message/?ordering=created_time/`,
  }).then(res => res.data)
}

// 发送信息
export const sendMessage = params => {
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/chat/${params.id.replace(/-/g, "")}/message/`,
    data: Qs.stringify(params)
  }).then(res => res.data)
}
// 增加对话
export const CreateChat = params => {
  return axios({
    method: 'post',
    baseURL: `${baseUrl}/chat/box/`,
    data: Qs.stringify(params)
  }).then(res => res.data)
}

export function DeleteChat(id) {
  return axios({
    method: 'delete',
    baseURL: `${baseUrl}/chat/${id}/box/`,
  }).then(res => res.data)
}
// export const DeleteChat = params => {
//   return axios({
//     method: 'delete',
//     baseURL: `http://localhost:8000/chat/box/`,
//     data: params
//   }).then(res => res.data)
// }
