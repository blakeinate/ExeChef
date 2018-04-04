import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Headers, Http, Response, URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { JwtService} from "./jwt.service";

@Injectable()
export class ApiService {
  constructor(
    private http: Http,
    private jwtService: JwtService
  ) {}

  private setHeaders(): Headers {
    let headersConfig = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    // let token = this.jwtService.getToken();
    // if(token){
    //   headersConfig['Authorization'] = `Token ${token}`;
    // }

    return new Headers(headersConfig);
  }

  private formatErrors(error: Response) {
     return Observable.throw(error.json());
  }

  post(path: string, body: Object = {}): Observable<any> {
    console.log(JSON.stringify(body));
    return this.http.post(`${environment.api_url}${path}`, JSON.stringify(body), { headers: this.setHeaders() })
        .catch(this.formatErrors)
        .map((res:Response) => res.json());
  }

  get(path: string, params: URLSearchParams = new URLSearchParams()): Observable<any> {
   return this.http.get(`${environment.api_url}${path}`, { headers: this.setHeaders(), search: params })
    .catch(this.formatErrors)
    .map((res:Response) => res.json());
}

}
