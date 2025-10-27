<template>
  <div class="space-y-8">
    <!-- Top Search Block -->
    <section
      class="bg-[#F7A86B] shadow-sm p-6 rounded-2xl flex flex-col lg:flex-row items-stretch gap-6"
    >
      <!-- Левая часть -->
      <div class="lg:w-1/3 flex items-center">
        <h2 class="text-xl font-semibold text-gray-900 leading-snug">
          Find the perfect partner for your project
        </h2>
      </div>

      <!-- Правая часть -->
      <div
        class="bg-white rounded-2xl flex flex-col lg:flex-row items-center justify-between gap-4 min-w-fit w-full lg:w-2/3 p-6"
      >
        <div class="flex flex-col gap-3 w-full">
          <div
            class="flex items-center border border-black rounded-full px-4 py-2 flex-1"
          >
            <UIcon name="mdi:magnify" size="20" class="text-gray-600 mr-2" />
            <input
              type="text"
              placeholder="Search web developers, SEO, UX..."
              class="flex-1 bg-transparent outline-none placeholder:text-gray-500 text-gray-800"
            />
          </div>

          <div
            class="flex items-center border border-black rounded-full px-4 py-2 flex-1"
          >
            <UIcon
              name="mdi:map-marker-outline"
              size="20"
              class="text-gray-600 mr-2"
            />
            <input
              type="text"
              placeholder="Any location"
              class="flex-1 bg-transparent outline-none placeholder:text-gray-500 text-gray-800"
            />
          </div>
        </div>

        <div class="min-w-fit w-1/3 flex justify-center">
          <button
            class="border border-black rounded-md px-5 py-2 font-medium text-gray-900 hover:bg-black hover:text-white transition"
          >
            Find a Vendor
          </button>
        </div>
      </div>
    </section>

    <!-- My Projects -->
    <section class="bg-white rounded-2xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold mb-4">My Projects</h3>
      <div class="flex flex-col md:flex-row gap-6">
        <UIcon name="icon-park-outline:list" size="50" class="text-gray-700" />
        <div>
          <div class="mb-4">
            <h4 class="text-xl font-semibold">
              Build a project brief in minutes
            </h4>
            <p class="text-gray-700 mt-1">
              Create a personalized project brief and send it to multiple
              best-fit vendors all at once.
            </p>
          </div>
          <MultiStepModal
            :steps="steps"
            title="Project Brief"
            @finish="handleFinish"
          >
            <template #step="{ step, answers, stepIndex }">
              <div class="w-full max-w-xl">
                <!-- Textarea for multi-line input -->
                <textarea
                  v-if="step.type === 'textarea'"
                  v-model="answers[stepIndex]"
                  :placeholder="step.placeholder"
                  class="w-full border border-gray-400 rounded-lg px-4 py-3 h-32 resize-none focus:outline-none focus:ring-2 focus:ring-gray-500"
                />

                <!-- Input for single-line input -->
                <input
                  v-else-if="step.type === 'input'"
                  v-model="answers[stepIndex]"
                  :placeholder="step.placeholder"
                  class="w-full border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
                />

                <!-- Options for multiple choice -->
                <div
                  v-else-if="step.type === 'options'"
                  class="flex justify-center gap-3"
                  :class="[step.optionsColumns ? 'flex-col' : 'flex-row']"
                >
                  <button
                    v-for="option in step.options"
                    :key="option"
                    class="border border-gray-600 rounded-md px-4 py-2 font-medium transition"
                    :class="[
                      answers[stepIndex] === option
                        ? 'bg-gray-800 text-white border-gray-800'
                        : 'hover:bg-gray-100 text-gray-800',
                    ]"
                    @click="answers[stepIndex] = option"
                  >
                    {{ option }}
                  </button>
                </div>

                <!-- Input with Checkbox -->
                <div
                  v-else-if="step.type === 'inputWithCheckbox'"
                  class="flex flex-col items-center gap-2"
                >
                  <input
                    v-model="answers[stepIndex]"
                    :placeholder="step.placeholder"
                    :disabled="answers[stepIndex + '_noWebsite']"
                    class="w-full border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  />
                  <label class="flex items-center gap-2 text-sm text-gray-700">
                    <input
                      v-model="answers[stepIndex + '_noWebsite']"
                      type="checkbox"
                    />
                    {{ step.checkboxLabel }}
                  </label>
                </div>

                <!-- Double Input (e.g., Company Name + Description) -->
                <div
                  v-else-if="step.type === 'doubleInput'"
                  class="flex flex-col gap-5 w-full"
                >
                  <input
                    v-model="answers[stepIndex + '_name']"
                    :placeholder="step.fields[0].placeholder"
                    class="border border-gray-400 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-gray-500"
                  />
                  <textarea
                    v-model="answers[stepIndex + '_about']"
                    :placeholder="step.fields[1].placeholder"
                    class="border border-gray-400 rounded-lg px-4 py-3 h-24 resize-none focus:outline-none focus:ring-2 focus:ring-gray-500"
                  />
                </div>
              </div>
            </template>
          </MultiStepModal>
        </div>
      </div>
    </section>

    <!-- My Recommendations -->
    <section class="bg-white rounded-2xl p-6 shadow-sm">
      <h3 class="text-lg font-semibold mb-4">My Recommendations</h3>
      <div class="grid lg:grid-cols-2 xl:grid-cols-3 gap-3">
        <div
          v-for="review in displayedReviews"
          :key="review.id"
          class="border border-gray-300 rounded-lg p-3 bg-gray-50"
        >
          <div class="flex items-center justify-between mb-1">
            <span class="font-semibold text-sm text-gray-900">{{
              review.commentedCompany
            }}</span>
            <div class="flex items-center gap-0.5 text-yellow-500 text-xs">
              <StarRating :rating="review.rating" />
            </div>
          </div>
          <p class="text-sm text-gray-700 leading-snug line-clamp-3">
            {{ review.text }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
interface Step {
  title: string;
  type: 'input' | 'textarea' | 'options' | 'inputWithCheckbox' | 'doubleInput';
  placeholder: string;
}

const myReviews = [
  {
    id: 1,
    commentedCompany: 'Acme Corp',
    rating: 5,
    text: 'They delivered our project ahead of time and exceeded expectations.',
  },
  {
    id: 2,
    commentedCompany: 'Beta LLC',
    rating: 4,
    text: 'Very professional team, great communication throughout the process.',
  },
  {
    id: 3,
    commentedCompany: 'Gamma Inc',
    rating: 5,
    text: 'Excellent work on our UI/UX design — creative and detail-oriented.',
  },
];

const displayedReviews = computed(() => myReviews?.slice(0, 3) || []);

function handleFinish(data) {
  console.log('📦 Итоговые ответы:', data);

  // пример: отправка на сервер
  // fetch('/api/brief', {
  //   method: 'POST',
  //   headers: { 'Content-Type': 'application/json' },
  //   body: JSON.stringify(data),
  // })
  //   .then((r) => r.json())
  //   .then((res) => {
  //     console.log('✅ Успешно отправлено:', res);
  //   })
  //   .catch((err) => console.error('❌ Ошибка при отправке:', err));
}

const steps: Step[] = [
  {
    title: "What's your project about? What goals do you want to accomplish?",
    type: 'textarea',
    placeholder:
      'E.g., Optimize website for faster performance / Grow website traffic through targeted keyword optimization / Make my website navigation more user friendly.',
  },
  // {
  //   title: 'What kind of company are you looking for?',
  //   type: 'input',
  //   placeholder: 'Search for SEO, web development, etc.',
  // },
  // {
  //   title: 'When would you like to start this project?',
  //   type: 'options',
  //   options: ['Within 30 days', 'Within 60 days', 'After 60+ days'],
  // },
  // {
  //   title: "What's important to you about a provider's location?",
  //   type: 'options',
  //   options: [
  //     'No preference — just looking for the best providers',
  //     'Near me for in-person collaboration',
  //     'I have specific countries in mind',
  //   ],
  //   optionsColumns: true,
  // },
  // {
  //   title: "What's your company's website?",
  //   type: 'inputWithCheckbox',
  //   placeholder: 'www.yourcompany.com',
  //   checkboxLabel: 'I don’t have a website yet',
  // },
  // {
  //   title: "What's your company name?",
  //   type: 'doubleInput',
  //   fields: [
  //     { label: 'Company Name', placeholder: 'Company Name' },
  //     {
  //       label: "What's your business about?",
  //       placeholder:
  //         'Consider including basic details like name, industry, and what makes your business unique and valuable to your target audience.',
  //       textarea: true,
  //     },
  //   ],
  // },
];
</script>
