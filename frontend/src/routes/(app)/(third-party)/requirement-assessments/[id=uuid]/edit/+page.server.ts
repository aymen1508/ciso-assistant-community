import { handleErrorResponse, nestedWriteFormAction } from '$lib/utils/actions';
import { BASE_API_URL } from '$lib/utils/constants';
import { getModelInfo, urlParamModelVerboseName } from '$lib/utils/crud';
import { getSecureRedirect } from '$lib/utils/helpers';
import { modelSchema } from '$lib/utils/schemas';
import { listViewFields } from '$lib/utils/table';
import * as m from '$paraglide/messages';
import { tableSourceMapper } from '@skeletonlabs/skeleton';
import type { Actions } from '@sveltejs/kit';
import { fail, redirect } from '@sveltejs/kit';
import { setFlash } from 'sveltekit-flash-message/server';
import { superValidate } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import type { PageServerLoad } from './$types';
import { z } from 'zod';

export const load = (async ({ fetch, params }) => {
	const URLModel = 'requirement-assessments';
	const baseUrl = BASE_API_URL;
	const endpoint = `${baseUrl}/${URLModel}/${params.id}/`;

	async function fetchJson(url: string) {
		const res = await fetch(url);
		if (!res.ok) {
			console.error(`Failed to fetch data from ${url}: ${res.statusText}`);
			return null;
		}
		return res.json();
	}

	const requirementAssessment = await fetchJson(endpoint);
	const requirement = requirementAssessment.requirement;
	const compliance_assessment_score = await fetchJson(
		`${baseUrl}/compliance-assessments/${requirementAssessment.compliance_assessment.id}/global_score/`
	);

	const parent = requirementAssessment.requirement.parent_requirement;

	const model = getModelInfo(URLModel);
	const object = { ...requirementAssessment };
	Object.keys(object).forEach((key) => {
		if (object[key] instanceof Object && 'id' in object[key]) {
			object[key] = object[key].id;
		}
	});

	const schema = modelSchema(URLModel);
	object.evidences = object.evidences.map((evidence) => evidence.id);
	const form = await superValidate(object, zod(schema), { errors: true });

	const selectOptions: Record<string, any> = {};
	if (model.selectFields) {
		await Promise.all(
			model.selectFields.map(async (selectField) => {
				const url = `${baseUrl}/${URLModel}/${selectField.field}/`;
				const data = await fetchJson(url);
				if (data) {
					selectOptions[selectField.field] = Object.entries(data).map(([key, value]) => ({
						label: value,
						value: selectField.valueType === 'number' ? parseInt(key) : key
					}));
				}
			})
		);
	}
	model.selectOptions = selectOptions;

	const measureCreateSchema = modelSchema('applied-controls');
	const measureCreateForm = await superValidate(
		{ folder: requirementAssessment.folder.id },
		zod(measureCreateSchema),
		{ errors: false }
	);

	const measureModel = getModelInfo('applied-controls');

	const measureSelectOptions: Record<string, any> = {};
	if (measureModel.selectFields) {
		await Promise.all(
			measureModel.selectFields.map(async (selectField) => {
				const url = `${baseUrl}/applied-controls/${selectField.field}/`;
				const data = await fetchJson(url);
				if (data) {
					measureSelectOptions[selectField.field] = Object.entries(data).map(([key, value]) => ({
						label: value,
						value: selectField.valueType === 'number' ? parseInt(key) : key
					}));
				} else {
					console.error(`Failed to fetch data for ${selectField.field}: ${response.statusText}`);
				}
			})
		);
	}

	measureModel['selectOptions'] = measureSelectOptions;

	const tables: Record<string, any> = {};

	await Promise.all(
		['applied-controls', 'evidences'].map(async (key) => {
			const keyEndpoint = `${BASE_API_URL}/${key}/?requirement_assessments=${params.id}`;
			const response = await fetch(keyEndpoint);

			if (response.ok) {
				const data = await response.json().then((data) => data.results);

				const bodyData = tableSourceMapper(data, listViewFields[key].body);

				const table: TableSource = {
					head: listViewFields[key].head,
					body: bodyData,
					meta: data
				};
				tables[key] = table;
			} else {
				console.error(`Failed to fetch data for ${key}: ${response.statusText}`);
			}
		})
	);

	const evidenceModel = getModelInfo('evidences');
	const evidenceCreateSchema = modelSchema('evidences');
	const evidenceCreateForm = await superValidate(
		{ requirement_assessments: [params.id], folder: requirementAssessment.folder.id },
		zod(evidenceCreateSchema),
		{ errors: false }
	);

	const evidenceSelectOptions: Record<string, any> = {};
	if (evidenceModel.selectFields) {
		await Promise.all(
			evidenceModel.selectFields.map(async (selectField) => {
				const url = `${baseUrl}/evidences/${selectField.field}/`;
				const data = await fetchJson(url);
				if (data) {
					evidenceSelectOptions[selectField.field] = Object.entries(data).map(([key, value]) => ({
						label: value,
						value: selectField.valueType === 'number' ? parseInt(key) : key
					}));
				}
			})
		);
	}
	evidenceModel.selectOptions = evidenceSelectOptions;

	return {
		URLModel,
		title: requirementAssessment.name,
		requirementAssessment,
		compliance_assessment_score,
		requirement,
		parent,
		model,
		form,
		measureCreateForm,
		measureModel,
		evidenceModel,
		evidenceCreateForm,
		tables
	};
}) satisfies PageServerLoad;

export const actions: Actions = {
	updateRequirementAssessment: async (event) => {
		const URLModel = 'requirement-assessments';
		const schema = modelSchema(URLModel);
		const endpoint = `${BASE_API_URL}/${URLModel}/${event.params.id}/`;
		const form = await superValidate(event.request, zod(schema));

		if (!form.valid) {
			console.log(form.errors);
			return fail(400, { form: form });
		}

		const requestInitOptions: RequestInit = {
			method: 'PUT',
			body: JSON.stringify(form.data)
		};

		const response = await event.fetch(endpoint, requestInitOptions);

		if (!response.ok) return handleErrorResponse({ event, response, form });

		const object = await response.json();
		const model: string = urlParamModelVerboseName(URLModel);
		setFlash({ type: 'success', message: m.successfullySavedObject({ object: model }) }, event);
		redirect(
			302,
			getSecureRedirect(event.url.searchParams.get('next')) ||
				`/compliance-assessments/${object.compliance_assessment}/`
		);
	},
	createAppliedControl: async (event) => {
		const URLModel = 'applied-controls';
		const schema = modelSchema(URLModel);
		const endpoint = `${BASE_API_URL}/${URLModel}/`;
		const form = await superValidate(event.request, zod(schema));

		if (!form.valid) {
			console.log(form.errors);
			return fail(400, { form: form });
		}

		const requestInitOptions: RequestInit = {
			method: 'POST',
			body: JSON.stringify(form.data)
		};

		const response = await event.fetch(endpoint, requestInitOptions);

		if (!response.ok) return handleErrorResponse({ event, response, form });

		const measure = await response.json();

		const requirementAssessmentEndpoint = `${BASE_API_URL}/requirement-assessments/${event.params.id}/`;
		const requirementAssessment = await event
			.fetch(`${requirementAssessmentEndpoint}object`)
			.then((res) => res.json());

		const measures = [...requirementAssessment.applied_controls, measure.id];

		const patchRequestInitOptions: RequestInit = {
			method: 'PATCH',
			body: JSON.stringify({ applied_controls: measures })
		};

		const patchRes = await event.fetch(requirementAssessmentEndpoint, patchRequestInitOptions);
		if (!patchRes.ok) return handleErrorResponse({ event, response: patchRes, form });

		const model: string = urlParamModelVerboseName(URLModel);
		setFlash(
			{
				type: 'success',
				message: m.successfullyUpdatedObject({ object: model })
			},
			event
		);
		return { form, newControl: measure.id };
	},
	createEvidence: async (event) => {
		const result = await nestedWriteFormAction({ event, action: 'create' });
		return { form: result.form, newEvidence: result.object.id };
	},
	createSuggestedControls: async (event) => {
		const formData = await event.request.formData();

		if (!formData) {
			return fail(400, { form: null });
		}

		const schema = z.object({ id: z.string().uuid() });
		const form = await superValidate(formData, zod(schema));

		const response = await event.fetch(
			`/requirement-assessments/${event.params.id}/suggestions/applied-controls`,
			{
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			}
		);
		if (response.ok) {
			setFlash(
				{
					type: 'success',
					message: m.createAppliedControlsFromSuggestionsSuccess()
				},
				event
			);
		} else {
			setFlash(
				{
					type: 'error',
					message: m.createAppliedControlsFromSuggestionsError()
				},
				event
			);
		}
		return { form };
	}
};
