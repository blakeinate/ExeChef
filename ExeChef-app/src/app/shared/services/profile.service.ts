import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Rx';

import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { ApiService } from './api.service';
import { Profile } from '../models';

@Injectable()
export class ProfilesService {
  constructor (
    private apiService: ApiService
  ) {}

  get(username: string): Observable<Profile> {
    console.log("this is the user name we are getting ",username);
    return this.apiService.get('/User/' + username)
      .map((data) =>{
        console.log(data)
        return data;
      })
      //.catch(this.formatErrors);
  }

  follow(followList: string[]):Observable<Profile>{
    return this.apiService.put("/User",{"followed":followList});
  }

  // unfollow(username: string):Observable<Profile>{
  //   return this.apiService.put("/User",{"unfollowed":username});
  // }



   formatErrors(error: Response) {
     console.log(error);
     return Observable.throw(error.json());
  }
}
