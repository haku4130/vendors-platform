<template>
  <AuthFormContainer>
    <div class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-gray-800">Register</h2>
      <h2 class="text-sm mb-6 text-gray-600">
        Create an account to start using Vendor Platform
      </h2>
    </div>

    <UForm :schema="schema" :state="state" class="space-y-4" @submit="onSubmit">
      <UFormField label="First Name" name="firstName">
        <UInput v-model="state.firstName" class="w-full bg-transparent" />
      </UFormField>
      <UFormField label="Last Name" name="lastName">
        <UInput v-model="state.lastName" class="w-full" />
      </UFormField>
      <UFormField label="Company Name" name="companyName">
        <UInput v-model="state.companyName" class="w-full" />
      </UFormField>
      <UFormField label="Email" name="email">
        <UInput v-model="state.email" class="w-full" />
      </UFormField>

      <UFormField label="Password" name="password">
        <UInput
          v-model="state.password"
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
        label="Create account"
        class="font-semibold justify-center py-2 px-10 rounded-lg mt-4"
        type="submit"
      />
    </UForm>

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
type UserStatus = 'vendor' | 'client';

const router = useRouter();

defineProps<{
  role: UserStatus;
}>();

const state = ref({
  firstName: '',
  lastName: '',
  companyName: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const schema =
  process.env.NODE_ENV === 'development'
    ? null
    : v.pipe(
        v.object({
          firstName: v.pipe(v.string(), v.nonEmpty('This field is required')),
          lastName: v.pipe(v.string(), v.nonEmpty('This field is required')),
          companyName: v.pipe(v.string(), v.nonEmpty('This field is required')),
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
type Schema = v.InferOutput<typeof schema>;

const toast = useToast();
async function onSubmit(event: FormSubmitEvent<Schema>) {
  toast.add({
    title: 'Success',
    description: 'The form has been submitted.',
    color: 'success',
  });
  console.log(event.data);
  router.push('/choose-role');
}

const show = ref(false);
</script>
