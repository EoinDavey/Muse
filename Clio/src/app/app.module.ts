import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import {CodemirrorModule} from '@ctrl/ngx-codemirror';
import {FormsModule} from '@angular/forms';
import {HomeComponent} from './home/home.component';
import {CoreComponent} from './editor/core/core.component';
import { EditorComponent } from './editor/editor.component';
import {RouterModule} from '@angular/router';
import {HttpClientModule} from '@angular/common/http';
import {HotkeyModule} from 'angular2-hotkeys';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    CoreComponent,
    EditorComponent
  ],
  imports: [
    BrowserModule,
    CodemirrorModule,
    HttpClientModule,
    FormsModule,
    HotkeyModule.forRoot(),
    RouterModule.forRoot([
      { path: 'home', pathMatch: 'full', component: HomeComponent},
      { path: 'editor', pathMatch: 'full', component: EditorComponent},
      { path: '**', pathMatch: 'full', redirectTo: '/home'},
      { path: '', pathMatch: 'full', redirectTo: '/home'}
    ])
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
