import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {ICodeSubmission} from '../../models/ICodeSubmission';
import {IAudioResponse} from '../../models/IAudioResponse';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HttpService {
  museUrl: string;
  revAiUrl: string;

  constructor(private http: HttpClient) { }

  // TODO: Add headers as necessary
  sendCode(codeSubmission: ICodeSubmission): Observable<IAudioResponse> {
    return this.http.post<IAudioResponse>(`${this.museUrl}`, codeSubmission);
  }

  sendAudio(codeSubmission: ICodeSubmission): Observable<IAudioResponse> {
    return this.http.post<IAudioResponse>(`${this.museUrl}`, codeSubmission);
  }
}
