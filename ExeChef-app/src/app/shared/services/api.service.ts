import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import { Headers, Http, Response, URLSearchParams } from '@angular/http';
import { Observable } from 'rxjs/Rx';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/catch';

import { JwtService} from "./jwt.service";

/// to do
// add delete request for logout route.
@Injectable()
export class ApiService {
  constructor(
    private http: Http,
    private jwtService: JwtService
  ) {}

  private setHeaders(refresh: Boolean = false): Headers {
    let headersConfig = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    let token = this.jwtService.getToken();
    if(refresh){
      token = this.jwtService.getRefreshToken();
    }
    if(token){
      headersConfig['Authorization'] = `Bearer ${token}`;
    }

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

  postRefresh(path: string, body: Object = {}): Observable<any> {
    console.log(JSON.stringify(body));
    return this.http.post(`${environment.api_url}${path}`, JSON.stringify(body), { headers: this.setHeaders(true) })
        .catch(this.formatErrors)
        .map((res:Response) => res.json());
  }

  get(path: string, params: URLSearchParams = new URLSearchParams()): Observable<any> {
   return this.http.get(`${environment.api_url}${path}`, { headers: this.setHeaders(), search: params })
    .catch(this.formatErrors)
    .map((res:Response) => res.json());
  }

  getRefresh(path: string, params: URLSearchParams = new URLSearchParams()): Observable<any> {
   return this.http.get(`${environment.api_url}${path}`, { headers: this.setHeaders(true), search: params })
    .catch(this.formatErrors)
    .map((res:Response) => res.json());
  }

  put(path: string, body: Object = {}): Observable<any> {
    return this.http.put( `${environment.api_url}${path}`, JSON.stringify(body), { headers: this.setHeaders() })
        .catch(this.formatErrors)
        .map((res:Response) => res.json());
  }


}
