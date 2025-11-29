<template>
  <AuthFormContainer>
    <div class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-gray-800">Register</h2>
      <h2 class="text-sm mb-6 text-gray-600">
        Create an account to start using Vendor Platform
      </h2>
    </div>

    <UStepper
      ref="stepper"
      :items="items"
      disabled
      class="w-full gap-0"
      :ui="{ item: 'hidden' }"
    >
      <template #registration>
        <UForm
          :schema="schema"
          :state="state"
          class="space-y-4"
          @submit="stepper?.next()"
        >
          <UFormField label="Full Name" name="fullName">
            <UInput
              v-model="state.fullName"
              leading-icon="i-lucide-user"
              class="w-full"
            />
          </UFormField>
          <UFormField label="Company Name" name="companyName">
            <UInput
              v-model="state.companyName"
              leading-icon="i-lucide-building"
              class="w-full"
            />
          </UFormField>
          <UFormField label="Company Location" name="companyLocation">
            <LocationSelector v-model="state.companyLocation" class="w-full" />
          </UFormField>
          <UFormField label="Email" name="email">
            <UInput
              v-model="state.email"
              leading-icon="i-lucide-at-sign"
              class="w-full"
            />
          </UFormField>

          <UFormField label="Password" name="password">
            <UInput
              v-model="state.password"
              leading-icon="i-lucide-lock"
              class="w-full"
              :type="show ? 'text' : 'password'"
              :ui="{ trailing: 'pe-1' }"
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                  :aria-label="show ? 'Hide password' : 'Show password'"
                  :aria-pressed="show"
                  aria-controls="password"
                  @click="show = !show"
                />
              </template>
            </UInput>
          </UFormField>
          <UFormField label="Confirm Password" name="confirmPassword">
            <UInput
              v-model="state.confirmPassword"
              leading-icon="i-lucide-lock"
              class="w-full"
              :type="show ? 'text' : 'password'"
              :ui="{ trailing: 'pe-1' }"
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                  :aria-label="show ? 'Hide password' : 'Show password'"
                  :aria-pressed="show"
                  aria-controls="password"
                  @click="show = !show"
                />
              </template>
            </UInput>
          </UFormField>

          <UButton
            variant="solid"
            color="warning"
            size="lg"
            label="Next Step"
            class="font-semibold justify-center py-2 px-10 rounded-lg mt-4"
            type="submit"
          />
        </UForm>
      </template>

      <template #role-selection>
        <UForm :schema="schema" :state="state" @submit="onSubmit">
          <UFormField>
            <URadioGroup
              v-model="state.role"
              indicator="hidden"
              variant="card"
              orientation="vertical"
              :items="roleSelectionOptions"
              class="w-fit m-auto"
              :ui="{
                fieldset: 'gap-y-3',
                item: 'has-data-[state=checked]:bg-primary/5',
                label: 'font-bold',
                description: 'text-normal mt-2',
              }"
            />
          </UFormField>

          <div class="flex justify-between gap-2 mt-8">
            <UButton
              variant="soft"
              size="lg"
              label="Go Back"
              class="flex-1 font-semibold justify-center py-2 rounded-lg"
              @click="stepper?.prev()"
            />

            <UButton
              variant="solid"
              color="warning"
              size="lg"
              label="Create account"
              class="flex-1 font-semibold justify-center py-2 rounded-lg"
              type="submit"
              :disabled="!state.role"
            />
          </div>
        </UForm>
      </template>
    </UStepper>

    <p class="text-sm text-gray-800 mt-4">
      Have an account?
      <NuxtLink
        to="/sign-in"
        class="font-semibold underline hover:text-gray-900"
      >
        Sign In
      </NuxtLink>
    </p>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import * as v from 'valibot';
import type { FormSubmitEvent } from '@nuxt/ui';

import { usersRegisterUser, loginLoginAccessToken } from '~/generated/api';
import type { UserRole } from '~/generated/api';

const stepper = useTemplateRef('stepper');

const state = ref({
  fullName: '',
  companyName: '',
  companyLocation: '',
  email: '',
  password: '',
  confirmPassword: '',
  role: '',
});

const schemaDefinition = v.pipe(
  v.object({
    fullName: v.pipe(v.string(), v.nonEmpty('This field is required')),
    companyName: v.pipe(v.string(), v.nonEmpty('This field is required')),
    companyLocation: v.pipe(v.string(), v.nonEmpty('This field is required')),
    email: v.pipe(v.string(), v.email('Invalid email')),
    password: v.pipe(
      v.string(),
      v.minLength(8, 'Must be at least 8 characters')
    ),
    confirmPassword: v.string(),
  }),
  v.forward(
    v.partialCheck(
      [['password'], ['confirmPassword']],
      (input) => input.password === input.confirmPassword,
      'Passwords do not match'
    ),
    ['confirmPassword']
  )
);

type Schema = v.InferOutput<typeof schemaDefinition>;

const schema = schemaDefinition;

const toast = useToast();
const token = useCookie('access_token');
const auth = useAuth();

async function onSubmit(event: FormSubmitEvent<Schema>) {
  const { email, password, fullName, companyName, companyLocation } =
    event.data;

  const register = await usersRegisterUser({
    body: {
      email,
      password,
      full_name: fullName,
      company_name: companyName,
      location: companyLocation,
      role: state.value.role as UserRole,
    },
  });

  if (register.error) {
    const detail =
      typeof register.error.detail === 'string'
        ? register.error.detail
        : Array.isArray(register.error.detail)
          ? (register.error.detail[0]?.msg ?? 'Registration failed')
          : 'Registration failed';

    toast.add({
      title: 'Registration failed',
      description: detail,
      color: 'error',
    });
    return;
  }

  const login = await loginLoginAccessToken({
    body: { username: email, password },
  });

  if (login.error) {
    toast.add({
      title: 'Error',
      description: 'Registered successfully, but failed to login.',
      color: 'warning',
    });
    return;
  }

  token.value = login.data.access_token;

  await auth.loadUser();

  toast.add({
    title: 'Welcome!',
    description: 'Your account has been created.',
    color: 'success',
  });

  navigateTo('/dashboard');
}

const show = ref(false);

const items = [
  {
    title: 'Registration',
    slot: 'registration',
  },
  {
    title: 'Role Selection',
    slot: 'role-selection',
  },
];

const roleSelectionOptions = [
  {
    label: 'Hire a business partner',
    value: 'company',
    description:
      'I want to find and hire a provider to help our company achieve our goals.',
  },
  {
    label: 'Get listed on the platform',
    value: 'vendor',
    description:
      "I want to sell my business' services and boost visibility for my brand.",
  },
];
</script>
