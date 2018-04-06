import {Injectable} from '@angular/core';


@Injectable()
export class JwtService{

  getToken(): String {
    // console.log(window.localStorage['jwtToken']);
    return window.localStorage['jwtToken'];

  }

  saveToken(token:String){
    window.localStorage['jwtToken'] = token;
  }

  getRefreshToken(): String {
    // console.log("coming from jwtService: get refresh token",window.localStorage['jwtRefreshToken']);
    return window.localStorage['jwtRefreshToken'];
  }

  saveRefreshToken(token:String){
    window.localStorage['jwtRefreshToken'] = token;
  }

  saveTokens(token:String,refreshToken:String){
    window.localStorage['jwtToken'] = token;
    window.localStorage['jwtRefreshToken'] = refreshToken;
  }

  destoryToken(){
    window.localStorage.removeItem('jwtToken');
    window.localStorage.removeItem('jwtRefreshToken');
  }

}
