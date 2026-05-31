<template>
  <div class="bg-white text-slate-800">
    <UHeader :to="$localePath('/')">
      <template #title>
        <div class="flex items-center gap-2 font-bold text-blue-600">
          <Logo />
          {{ $t('brandName') }}
        </div>
      </template>

      <UNavigationMenu :items="navItems" />

      <template #right>
        <LangSwitcher />
        <div class="hidden items-center gap-2 md:flex">
          <template v-if="auth.user.value">
            <UButton :to="$localePath('/dashboard/projects')">{{
              $t('nav.dashboard')
            }}</UButton>
          </template>
          <template v-else>
            <UButton :to="$localePath('/sign-in')">{{
              $t('nav.signIn')
            }}</UButton>
            <UButton :to="$localePath('/register')" variant="solid">{{
              $t('nav.getStarted')
            }}</UButton>
          </template>
        </div>
      </template>

      <template #body>
        <UNavigationMenu
          :items="navItems"
          orientation="vertical"
          class="mb-2"
        />
        <div class="flex flex-col gap-2 px-2.5 pb-4">
          <template v-if="auth.user.value">
            <UButton :to="$localePath('/dashboard/projects')" block>{{
              $t('nav.dashboard')
            }}</UButton>
          </template>
          <template v-else>
            <UButton :to="$localePath('/sign-in')" block>{{
              $t('nav.signIn')
            }}</UButton>
            <UButton :to="$localePath('/register')" variant="solid" block>{{
              $t('nav.getStarted')
            }}</UButton>
          </template>
        </div>
      </template>
    </UHeader>

    <section
      class="relative overflow-hidden bg-linear-to-br from-sky-50 to-sky-100 px-6 pb-10 pt-10 md:pt-16"
    >
      <div
        class="pointer-events-none absolute -right-52 -top-52 h-[500px] w-[500px] rounded-full bg-[radial-gradient(circle,rgba(37,99,235,0.1)_0%,transparent_70%)]"
      ></div>
      <div
        class="relative mx-auto grid max-w-7xl gap-12 md:grid-cols-2 md:items-center"
      >
        <div>
          <h1
            class="mb-6 text-2xl md:text-4xl font-extrabold leading-tight text-slate-800"
          >
            {{ $t('hero.titleBefore') }}
            <span class="text-blue-600">{{ $t('hero.highlight') }}</span>
            {{ $t('hero.titleAfter') }}
          </h1>
          <p class="mb-8 text-lg md:text-xl text-slate-500">
            {{ $t('hero.subtitle') }}
          </p>
          <div class="flex flex-wrap gap-4">
            <UButton :to="$localePath('/register')" variant="solid" size="xl">
              {{ $t('hero.placeProject') }}
            </UButton>
            <UButton
              :to="$localePath('/dashboard/vendor-registration')"
              size="xl"
            >
              {{ $t('hero.becomeVendor') }}
            </UButton>
          </div>
        </div>
        <div class="overflow-hidden rounded-2xl shadow-2xl shadow-black/15">
          <img
            src="https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=600&fit=crop"
            alt="IT команда за работой"
            class="h-full w-full object-cover"
            width="800"
            height="600"
          />
        </div>
      </div>
    </section>

    <section id="features" class="bg-slate-50 px-6 py-24">
      <div class="mx-auto max-w-7xl">
        <div class="mb-16 text-center">
          <h2 class="mb-4 text-2xl md:text-4xl font-extrabold text-slate-800">
            {{ $t('features.title') }}
          </h2>
          <p class="text-lg md:text-xl text-slate-500">
            {{ $t('features.subtitle') }}
          </p>
        </div>
        <div class="grid gap-8 md:grid-cols-2 xl:grid-cols-3">
          <article
            v-for="feature in features"
            :key="feature.title"
            class="rounded-2xl bg-white p-8 shadow transition hover:-translate-y-2 hover:shadow-xl"
          >
            <div class="mb-4 flex items-center gap-4">
              <div
                class="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-linear-to-br from-blue-600 to-sky-500"
              >
                <UIcon :name="feature.icon" class="h-6 w-6 text-white" />
              </div>
              <h3 class="text-xl font-semibold text-slate-800">
                {{ feature.title }}
              </h3>
            </div>
            <p class="text-slate-500">{{ feature.description }}</p>
          </article>
        </div>
      </div>
    </section>

    <section id="how-it-works" class="bg-white px-6 py-24">
      <div class="mx-auto max-w-7xl">
        <div class="mb-16 text-center">
          <h2 class="mb-4 text-2xl md:text-4xl font-extrabold text-slate-800">
            {{ $t('howItWorks.title') }}
          </h2>
          <p class="text-lg md:text-xl text-slate-500">
            {{ $t('howItWorks.subtitle') }}
          </p>
        </div>
        <UStepper
          :items="steps"
          default-value="step-1"
          orientation="vertical"
          :linear="false"
          disabled
          size="lg"
          class="mx-auto max-w-xl"
        />
      </div>
    </section>

    <section class="bg-slate-50 px-6 py-24">
      <div class="mx-auto max-w-7xl">
        <div class="mb-16 text-center">
          <h2 class="mb-4 text-2xl md:text-4xl font-extrabold text-slate-800">
            {{ $t('audience.title') }}
          </h2>
          <p class="text-lg md:text-xl text-slate-500">
            {{ $t('audience.subtitle') }}
          </p>
        </div>
        <div class="grid gap-12 md:grid-cols-2">
          <article
            v-for="group in audienceGroups"
            :key="group.title"
            class="rounded-2xl bg-white p-12 shadow"
          >
            <h3 class="mb-6 text-3xl font-bold text-blue-600">
              {{ group.title }}
            </h3>
            <ul>
              <li
                v-for="item in group.items"
                :key="item"
                class="flex gap-3 border-b border-slate-200 py-4 last:border-b-0"
              >
                <span class="text-xl font-bold text-emerald-500">✓</span>
                <span class="text-slate-700">{{ item }}</span>
              </li>
            </ul>
          </article>
        </div>
      </div>
    </section>

    <section
      id="clients"
      class="bg-linear-to-br from-slate-50 to-slate-200 px-6 py-24"
    >
      <div class="mx-auto max-w-7xl">
        <div class="mb-16 text-center">
          <h2 class="mb-4 text-2xl md:text-4xl font-extrabold text-slate-800">
            {{ $t('clients.title') }}
          </h2>
          <p class="text-lg md:text-xl text-slate-500">
            {{ $t('clients.subtitle') }}
          </p>
        </div>
        <UCarousel
          v-slot="{ item }"
          :items="companies"
          auto-scroll
          loop
          :ui="{ item: 'basis-1/2 sm:basis-1/3 md:basis-1/4 lg:basis-1/5' }"
        >
          <div
            class="mx-2 flex flex-col items-center gap-3 rounded-2xl bg-white px-4 py-5"
          >
            <div class="flex h-12 w-full items-center justify-center">
              <img
                :src="`https://img.logo.dev/${item.domain}?token=pk_ElSYR795S5u7kZQ85WABEQ`"
                :alt="item.name"
                class="max-h-12 w-auto object-contain"
                @error="
                  (e) => ((e.target as HTMLImageElement).style.display = 'none')
                "
              />
            </div>
            <span class="text-sm font-semibold text-slate-700">{{
              item.name
            }}</span>
          </div>
        </UCarousel>
      </div>
    </section>

    <section
      class="bg-linear-to-br from-blue-600/80 via-sky-600/70 to-indigo-300/60 px-6 py-24 text-center text-white"
    >
      <div class="mx-auto max-w-3xl">
        <h2 class="mb-6 text-2xl md:text-5xl font-extrabold">
          {{ $t('cta.title') }}
        </h2>
        <p class="mb-8 text-lg md:text-xl opacity-90">
          {{ $t('cta.subtitle') }}
        </p>
        <NuxtLink
          :to="$localePath('/register')"
          class="inline-block rounded-lg bg-white px-6 py-3 text-base font-semibold text-blue-600 transition hover:bg-white/90"
        >
          {{ $t('cta.button') }}
        </NuxtLink>
      </div>
    </section>

    <footer class="bg-slate-800 px-6 pb-8 pt-16 text-white">
      <div
        class="mx-auto mb-12 grid max-w-7xl gap-12 md:grid-cols-[2fr_1fr_1fr_1fr]"
      >
        <div>
          <h3 class="mb-4 text-3xl font-bold">{{ $t('brandName') }}</h3>
          <p class="text-white/70">{{ $t('footer.description') }}</p>
        </div>
        <div>
          <h4 class="mb-4 text-lg font-semibold">{{ $t('footer.product') }}</h4>
          <ul class="space-y-2">
            <li>
              <NuxtLink
                :to="$localePath('/search-process')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.searchProcess') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="$localePath('/pricing')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.pricing') }}
              </NuxtLink>
            </li>
            <li>
              <button
                class="text-white/70 transition hover:text-white text-left"
                @click="showApiToast"
              >
                {{ $t('pages.api') }}
              </button>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="mb-4 text-lg font-semibold">{{ $t('footer.company') }}</h4>
          <ul class="space-y-2">
            <li>
              <NuxtLink
                :to="$localePath('/about')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.about') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="$localePath('/contacts')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.contacts') }}
              </NuxtLink>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="mb-4 text-lg font-semibold">{{ $t('footer.legal') }}</h4>
          <ul class="space-y-2">
            <li>
              <NuxtLink
                :to="$localePath('/privacy')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.privacy') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="$localePath('/personal-data')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.personalData') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="$localePath('/recommendations-policy')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.recommendationsPolicy') }}
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="$localePath('/public-offer')"
                class="text-white/70 transition hover:text-white"
              >
                {{ $t('pages.publicOffer') }}
              </NuxtLink>
            </li>
          </ul>
        </div>
      </div>
      <div
        class="mx-auto max-w-7xl border-t border-white/10 pt-8 text-center text-white/70"
      >
        <p>{{ $t('footer.copyright', { year: year }) }}</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false });

const auth = useAuth();
const { t, tm, rt } = useI18n();
const toast = useToast();

useHead({ title: () => t('pageTitle') });

const year = new Date().getFullYear();

function showApiToast() {
  toast.add({
    title: t('footer.comingSoon'),
    icon: 'i-lucide-clock',
    color: 'info',
  });
}

function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
}

const navItems = computed(() => [
  { label: t('nav.features'), onSelect: () => scrollToSection('features') },
  {
    label: t('nav.howItWorks'),
    onSelect: () => scrollToSection('how-it-works'),
  },
  { label: t('nav.clients'), onSelect: () => scrollToSection('clients') },
]);

const companies = [
  { name: 'Лукойл', domain: 'lukoil.com' },
  { name: 'Газпром', domain: 'gazprom.com' },
  { name: 'Сбербанк', domain: 'sberbank.ru' },
  { name: 'ВТБ', domain: 'vtb.ru' },
  { name: 'Роснефть', domain: 'rosneft.com' },
  { name: 'МТС', domain: 'mts.ru' },
  { name: 'Яндекс', domain: 'ya.ru' },
  { name: 'РЖД', domain: 'rzd.ru' },
  { name: 'Мегафон', domain: 'megafon.ru' },
  { name: 'Ростех', domain: 'rostec.ru' },
];

const features = computed(() => [
  {
    icon: 'i-lucide-search',
    title: t('features.search.title'),
    description: t('features.search.description'),
  },
  {
    icon: 'i-lucide-file-text',
    title: t('features.briefs.title'),
    description: t('features.briefs.description'),
  },
  {
    icon: 'i-lucide-scale',
    title: t('features.compare.title'),
    description: t('features.compare.description'),
  },
  {
    icon: 'i-lucide-shield-check',
    title: t('features.verified.title'),
    description: t('features.verified.description'),
  },
  {
    icon: 'i-lucide-message-square',
    title: t('features.communication.title'),
    description: t('features.communication.description'),
  },
  {
    icon: 'i-lucide-bar-chart-2',
    title: t('features.analytics.title'),
    description: t('features.analytics.description'),
  },
]);

const steps = computed(() => [
  {
    value: 'step-1',
    title: t('howItWorks.step1.title'),
    description: t('howItWorks.step1.description'),
  },
  {
    value: 'step-2',
    title: t('howItWorks.step2.title'),
    description: t('howItWorks.step2.description'),
  },
  {
    value: 'step-3',
    title: t('howItWorks.step3.title'),
    description: t('howItWorks.step3.description'),
  },
]);

const audienceGroups = computed(() => [
  {
    title: t('audience.forCompanies.title'),
    items: (tm('audience.forCompanies.items') as unknown[]).map((item) =>
      rt(item),
    ),
  },
  {
    title: t('audience.forVendors.title'),
    items: (tm('audience.forVendors.items') as unknown[]).map((item) =>
      rt(item),
    ),
  },
]);
</script>
