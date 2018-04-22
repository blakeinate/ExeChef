import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService } from './api.service';
import { UserService} from './user.service';

import { Profile,User } from '../models';

@Injectable()
export class ProfilesService {
  constructor (
    private apiService: ApiService,
    private userService: UserService,
  ) {}

  get(username: string): Observable<Profile> {
    return this.apiService.get('/User/' + username)
      .map((data) =>{
        console.log(data)
        return data;
      })
  }


  toggleFollowing(username:string):Observable<User>{
    let following = this.userService.getCurrentUser().following;
    if(following == null){
      following = [];
    }
    var emit = false;
    if(!following.includes(username)){
        following.push(username);
        var emit = true;

    }else{

      following = following.filter(removeUserName => username !== removeUserName);
    }
    return this.userService.update({following:following}).map(data=>{
        //pass back a value for button to emit;
        data["emit"] = emit;
        return data;
    })
  }
}
