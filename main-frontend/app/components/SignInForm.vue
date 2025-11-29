<template>
  <AuthFormContainer class="max-w-sm">
    <div class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-gray-800">Sign In</h2>
      <h2 class="text-sm mb-6 text-gray-600">
        Welcome back to Vendor Platform
      </h2>
    </div>

    <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
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
        <template #hint>
          <NuxtLink
            to="/password-reset"
            class="font-semibold underline text-default hover:text-gray-900"
          >
            Forgot password?
          </NuxtLink>
        </template>
      </UFormField>

      <UButton
        type="submit"
        variant="solid"
        color="warning"
        size="lg"
        class="font-semibold justify-center py-2 px-10 rounded-lg my-4"
      >
        Continue
      </UButton>
    </UForm>

    <p class="text-sm text-gray-800">
      Don't have an account?
      <NuxtLink
        to="/register"
        class="font-semibold underline hover:text-gray-900"
      >
        Register
      </NuxtLink>
    </p>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import * as v from 'valibot';
import type { FormSubmitEvent } from '@nuxt/ui';
import { loginLoginAccessToken } from '~/generated/api';

const state = ref({
  email: '',
  password: '',
});

const schemaDefinition = v.pipe(
  v.object({
    email: v.pipe(v.string(), v.nonEmpty('This field is required')),
    password: v.pipe(v.string(), v.nonEmpty('This field is required')),
  })
);

type Schema = v.InferOutput<typeof schemaDefinition>;

// const schema = process.env.NODE_ENV === 'development' ? null : schemaDefinition;
const schema = schemaDefinition;

const toast = useToast();

async function onSubmit(event: FormSubmitEvent<Schema>) {
  const res = await loginLoginAccessToken({
    body: {
      username: event.data.email,
      password: event.data.password,
    },
  });

  if (!res.error) {
    const token = useCookie('access_token', {
      maxAge: 60 * 60 * 24 * 7,
      sameSite: 'strict',
    });
    token.value = res.data.access_token;

    toast.add({
      title: 'Success',
      description: 'Logged in successfully!',
      color: 'success',
    });

    navigateTo('/dashboard');
  } else {
    let detail: string;

    if (typeof res.error.detail === 'string') {
      detail = res.error.detail;
    } else if (Array.isArray(res.error.detail)) {
      detail = res.error.detail[0]?.msg ?? 'Something went wrong';
    } else {
      detail = 'Something went wrong';
    }

    toast.add({
      title: 'Login failed',
      description: detail,
      color: 'error',
    });
  }
}

const show = ref(false);
</script>
