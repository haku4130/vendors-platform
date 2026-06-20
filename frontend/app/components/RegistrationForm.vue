<template>
  <AuthFormContainer>
    <div class="text-start space-y-1">
      <h2 class="text-xl font-semibold text-white">
        {{ $t("auth.register.title") }}
      </h2>
      <h2 class="text-sm mb-6 text-gray-200">
        {{ $t("auth.register.subtitle") }}
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
          <UFormField :label="$t('auth.register.fullName')" name="fullName">
            <UInput
              v-model="state.fullName"
              leading-icon="i-lucide-user"
              class="w-full"
            />
          </UFormField>
          <UFormField
            :label="$t('auth.register.companyName')"
            name="companyName"
          >
            <UInput
              v-model="state.companyName"
              leading-icon="i-lucide-building"
              class="w-full"
            />
          </UFormField>
          <UFormField :label="$t('auth.register.inn')" name="inn">
            <UInput
              v-model="state.inn"
              leading-icon="i-lucide-hash"
              class="w-full"
            />
          </UFormField>
          <UFormField
            :label="$t('auth.register.companyLocation')"
            name="companyLocation"
          >
            <LocationSelector v-model="state.companyLocation" class="w-full" />
          </UFormField>
          <UFormField :label="$t('auth.register.email')" name="email">
            <UInput
              v-model="state.email"
              leading-icon="i-lucide-at-sign"
              class="w-full"
            />
          </UFormField>

          <UFormField :label="$t('auth.register.password')" name="password">
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
          <UFormField
            :label="$t('auth.register.confirmPassword')"
            name="confirmPassword"
          >
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

          <UFormField name="consent">
            <UCheckbox v-model="state.consent" :ui="{ label: 'text-start' }">
              <template #label>
                {{ $t("auth.register.consent") }}
                <NuxtLink
                  :to="$localePath('/privacy')"
                  target="_blank"
                  class="underline"
                  >{{ $t("auth.register.consentPrivacy") }}</NuxtLink
                >
              </template>
            </UCheckbox>
          </UFormField>
          <UFormField name="consentPersonalData">
            <UCheckbox
              v-model="state.consentPersonalData"
              :ui="{ label: 'text-start' }"
            >
              <template #label>
                {{ $t("auth.register.consentPersonalData") }}
                <NuxtLink
                  :to="$localePath('/personal-data')"
                  target="_blank"
                  class="underline"
                  >{{ $t("auth.register.consentPersonalDataLink") }}</NuxtLink
                >
              </template>
            </UCheckbox>
          </UFormField>

          <UButton
            variant="solid"
            color="primary"
            size="lg"
            :label="$t('auth.register.nextStep')"
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
              :label="$t('auth.register.goBack')"
              class="flex-1 font-semibold justify-center py-2 rounded-lg"
              @click="stepper?.prev()"
            />

            <UButton
              variant="solid"
              color="primary"
              size="lg"
              :label="$t('auth.register.submit')"
              class="flex-1 font-semibold justify-center py-2 rounded-lg"
              type="submit"
              :disabled="!state.role"
            />
          </div>
        </UForm>
      </template>
    </UStepper>

    <p class="text-sm text-gray-800 mt-4">
      {{ $t("auth.register.hasAccount") }}
      <NuxtLink
        :to="$localePath('/sign-in')"
        class="font-semibold underline hover:text-gray-900"
      >
        {{ $t("auth.register.signIn") }}
      </NuxtLink>
    </p>
  </AuthFormContainer>
</template>

<script setup lang="ts">
import * as v from "valibot";
import type { FormSubmitEvent } from "@nuxt/ui";

import { usersRegisterUser, loginLoginAccessToken } from "~/generated/api";
import type { UserRole } from "~/generated/api";

const { t } = useI18n();
const localePath = useLocalePath();
const stepper = useTemplateRef("stepper");

const state = ref({
  fullName: "",
  companyName: "",
  inn: "",
  companyLocation: "",
  email: "",
  password: "",
  confirmPassword: "",
  consent: false,
  consentPersonalData: false,
  role: "",
});

const schemaDefinition = v.pipe(
  v.object({
    fullName: v.pipe(v.string(), v.nonEmpty("This field is required")),
    companyName: v.pipe(v.string(), v.nonEmpty("This field is required")),
    inn: v.pipe(
      v.string(),
      v.nonEmpty("This field is required"),
      v.regex(/^\d{10}(\d{2})?$/, t("auth.register.innInvalid")),
    ),
    companyLocation: v.pipe(v.string(), v.nonEmpty("This field is required")),
    email: v.pipe(v.string(), v.email("Invalid email")),
    password: v.pipe(
      v.string(),
      v.minLength(8, "Must be at least 8 characters"),
    ),
    confirmPassword: v.string(),
    consent: v.pipe(
      v.boolean(),
      v.literal(true, t("auth.register.consentRequired")),
    ),
    consentPersonalData: v.pipe(
      v.boolean(),
      v.literal(true, t("auth.register.consentRequired")),
    ),
  }),
  v.forward(
    v.partialCheck(
      [["password"], ["confirmPassword"]],
      (input) => input.password === input.confirmPassword,
      "Passwords do not match",
    ),
    ["confirmPassword"],
  ),
);

type Schema = v.InferOutput<typeof schemaDefinition>;

const schema = schemaDefinition;

const toast = useToast();
const token = useCookie("access_token");
const auth = useAuth();

async function onSubmit(event: FormSubmitEvent<Schema>) {
  const { email, password, fullName, companyName, inn, companyLocation } =
    event.data;

  const register = await usersRegisterUser({
    body: {
      email,
      password,
      full_name: fullName,
      company_name: companyName,
      inn,
      location: companyLocation,
      role: state.value.role as UserRole,
    },
  });

  if (register.error) {
    toast.add({
      title: "Registration failed",
      description: extractErrorMessage(register.error),
      color: "error",
    });
    return;
  }

  const login = await loginLoginAccessToken({
    body: { username: email, password },
  });

  if (login.error) {
    toast.add({
      title: "Error",
      description: "Registered successfully, but failed to login.",
      color: "warning",
    });
    return;
  }

  token.value = login.data.access_token;

  await auth.loadUser();

  toast.add({
    title: "Welcome!",
    description: "Your account has been created.",
    color: "success",
  });

  navigateTo(localePath("/dashboard"));
}

const show = ref(false);

const items = [
  { title: "Registration", slot: "registration" },
  { title: "Role Selection", slot: "role-selection" },
];

const roleSelectionOptions = computed(() => [
  {
    label: t("auth.register.roles.company.label"),
    value: "company",
    description: t("auth.register.roles.company.description"),
  },
  {
    label: t("auth.register.roles.vendor.label"),
    value: "vendor",
    description: t("auth.register.roles.vendor.description"),
  },
]);
</script>
