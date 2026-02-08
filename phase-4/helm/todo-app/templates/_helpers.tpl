{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- range $key, $value := .Values.commonLabels }}
{{ $key }}: {{ $value | quote }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "todo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "todo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Backend deployment name
*/}}
{{- define "todo-app.backend.name" -}}
{{- printf "%s-backend" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend service name
*/}}
{{- define "todo-app.backend.serviceName" -}}
{{- printf "%s-backend-service" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend deployment name
*/}}
{{- define "todo-app.frontend.name" -}}
{{- printf "%s-frontend" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Frontend service name
*/}}
{{- define "todo-app.frontend.serviceName" -}}
{{- printf "%s-frontend-service" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
PostgreSQL service name
*/}}
{{- define "todo-app.postgresql.serviceName" -}}
{{- printf "%s-postgres-service" (include "todo-app.fullname" .) | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Backend image
*/}}
{{- define "todo-app.backend.image" -}}
{{- if .Values.global.imageRegistry }}
{{- printf "%s/%s:%s" .Values.global.imageRegistry .Values.backend.image.repository .Values.backend.image.tag }}
{{- else }}
{{- printf "%s:%s" .Values.backend.image.repository .Values.backend.image.tag }}
{{- end }}
{{- end }}

{{/*
Frontend image
*/}}
{{- define "todo-app.frontend.image" -}}
{{- if .Values.global.imageRegistry }}
{{- printf "%s/%s:%s" .Values.global.imageRegistry .Values.frontend.image.repository .Values.frontend.image.tag }}
{{- else }}
{{- printf "%s:%s" .Values.frontend.image.repository .Values.frontend.image.tag }}
{{- end }}
{{- end }}

{{/*
PostgreSQL image
*/}}
{{- define "todo-app.postgresql.image" -}}
{{- printf "%s/%s:%s" .Values.postgresql.image.registry .Values.postgresql.image.repository .Values.postgresql.image.tag }}
{{- end }}