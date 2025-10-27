<template>
  <div class="flex items-center justify-center">
    <div
      class="bg-[#F7A86B] rounded-xl shadow-md p-8 w-full max-w-sm text-center"
    >
      <p class="text-xl font-semibold">Join us</p>

      <hr class="my-4" />

      <form class="space-y-5" @submit.prevent="onSubmit">
        <!-- First Name -->
        <div>
          <label
            for="firstName"
            class="block font-semibold text-start text-gray-900 mb-1 pl-2"
          >
            First Name
          </label>
          <input
            id="firstName"
            v-model="form.firstName"
            type="text"
            class="w-full border border-black rounded-lg px-3 py-2 text-gray-900 bg-transparent focus:outline-none focus:ring-2 focus:ring-gray-700"
          />
        </div>

        <!-- Last Name -->
        <div>
          <label
            for="lastName"
            class="block font-semibold text-gray-900 mb-1 text-start pl-2"
          >
            Last Name
          </label>
          <input
            id="lastName"
            v-model="form.lastName"
            type="text"
            class="w-full border border-black rounded-lg px-3 py-2 text-gray-900 bg-transparent focus:outline-none focus:ring-2 focus:ring-gray-700"
          />
        </div>

        <!-- Work email -->
        <div>
          <label
            for="email"
            class="block font-semibold text-gray-900 mb-1 text-start pl-2"
          >
            Work email
          </label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            class="w-full border border-black rounded-lg px-3 py-2 text-gray-900 bg-transparent focus:outline-none focus:ring-2 focus:ring-gray-700"
          />
        </div>

        <!-- Password -->
        <div>
          <label
            for="password"
            class="block font-semibold text-gray-900 mb-1 text-start pl-2"
          >
            Password
          </label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            class="w-full border border-black rounded-lg px-3 py-2 text-gray-900 bg-transparent focus:outline-none focus:ring-2 focus:ring-gray-700"
          />
        </div>

        <!-- Confirm Password -->
        <div>
          <label
            for="confirmPassword"
            class="block font-semibold text-gray-900 mb-1 text-start pl-2"
          >
            Confirm Password
          </label>
          <input
            id="confirmPassword"
            v-model="form.confirmPassword"
            type="password"
            class="w-full border border-black rounded-lg px-3 py-2 text-gray-900 bg-transparent focus:outline-none focus:ring-2 focus:ring-gray-700"
          />
        </div>

        <!-- Submit button -->
        <button
          type="submit"
          class="w-full bg-[#8B2E2E] hover:bg-[#A63B3B] text-white font-semibold py-2 rounded-lg transition"
        >
          Create account
        </button>
      </form>

      <p class="text-sm text-gray-800 mt-4">
        Have an account?
        <NuxtLink
          to="/login"
          class="font-semibold underline hover:text-gray-900"
        >
          Sign In
        </NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  role: {
    type: String, // "vendor" или "client"
    required: true,
  },
});

const form = ref({
  firstName: '',
  lastName: '',
  email: '',
  password: '',
  confirmPassword: '',
});

function onSubmit() {
  console.log(`Submitting form for ${props.role}`, form.value);
  // здесь можно вызывать API:
  // await $api.post(`/auth/register/${props.role}`, form.value)
}
</script>
