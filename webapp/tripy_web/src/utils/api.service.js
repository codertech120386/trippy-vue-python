import axios from 'axios';
import { URLS } from '../utils/constants';
import { TokenService } from '../utils/token.service';

var CancelToken = axios.CancelToken;
var cancelTokens = {};


const APIService = {
    post(url, data){
        return axios.post(URLS.API_URL + url, data)
    }
}

const AuthAPIService = {
    get(url, params, cancel_previous=false) {
        var headers = {
            Authorization: TokenService.getToken()
        }
        if(cancel_previous && cancelTokens[url] != undefined){
            cancelTokens[url]()
        }
        return axios.get(URLS.API_URL + url, {
            params: params,
            headers: headers,
            cancelToken: new CancelToken(c => {cancelTokens[url] = c})
        })
    },
    put(url, data) {
        var headers = {
            Authorization: TokenService.getToken()
        }
        return axios.put(URLS.API_URL + url, data, {
            headers: headers
        })
    },
    delete(url, data) {
        var headers = {
            Authorization: TokenService.getToken()
        }
        return axios.delete(URLS.API_URL + url, {
            data: data,
            headers: headers
        })
    },
    post(url, data) {
        var headers = {
            Authorization: TokenService.getToken()
        }
        return axios.post(URLS.API_URL + url, data, {
            headers: headers
        })
    }
}

export { APIService, AuthAPIService }
