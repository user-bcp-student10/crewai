// login-api.service.ts

import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Inject, Injectable, InjectionToken } from '@angular/core';
import { Observable } from 'rxjs';
import { LoginRequest, LoginResponse } from './login-api.model';

/**
 * La aplicación debe proporcionar el endpoint ya aprobado.
 * No se establece aquí una ruta por falta del contrato.
 */
export const LOGIN_API_ENDPOINT = new InjectionToken<string>(
  'LOGIN_API_ENDPOINT',
);

@Injectable({ providedIn: 'root' })
export class LoginApiService {
  constructor(
    private readonly http: HttpClient,
    @Inject(LOGIN_API_ENDPOINT) private readonly endpoint: string,
  ) {}

  login(request: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(this.endpoint, request);
  }
}

/**
 * Mensajes genéricos de UX. No usa el cuerpo del error ni afirma
 * que estos estados sean el catálogo contractual del endpoint.
 */
export function getLoginErrorMessage(error: unknown): string {
  if (!(error instanceof HttpErrorResponse)) {
    return 'No pudimos completar la solicitud. Inténtalo de nuevo más tarde.';
  }

  switch (error.status) {
    case 0:
      return 'No pudimos conectar con el servicio. Inténtalo de nuevo más tarde.';
    case 400:
      return 'No se pudo procesar la solicitud. Revisa los datos e inténtalo de nuevo.';
    case 401:
      return 'No se pudo iniciar sesión. Verifica los datos e inténtalo de nuevo.';
    case 403:
      return 'No tienes autorización para realizar esta acción.';
    case 404:
      return 'No se encontró el recurso solicitado.';
    case 409:
      return 'No se pudo completar la solicitud por un conflicto. Inténtalo de nuevo.';
    default:
      if (error.status >= 500 && error.status <= 599) {
        return 'Ocurrió un problema temporal. Inténtalo más tarde.';
      }

      return 'No pudimos completar la solicitud. Inténtalo de nuevo más tarde.';
  }
}