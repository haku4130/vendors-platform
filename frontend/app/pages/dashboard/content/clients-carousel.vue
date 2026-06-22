<template>
  <div class="space-y-6 max-w-2xl">
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-semibold">
        {{ $t("clientsCarousel.editTitle") }}
      </h1>
      <UButton
        icon="i-lucide-save"
        variant="solid"
        :loading="saving"
        @click="save"
      >
        {{ $t("content.save") }}
      </UButton>
    </div>

    <div class="space-y-3">
      <div
        v-for="(company, index) in companies"
        :key="index"
        class="flex items-center gap-3 p-3 border border-default rounded-lg bg-white"
      >
        <div class="w-10 h-10 shrink-0 flex items-center justify-center">
          <img
            v-if="company.domain"
            :src="`https://img.logo.dev/${company.domain}?token=pk_ElSYR795S5u7kZQ85WABEQ`"
            :alt="company.name"
            class="max-h-8 w-auto object-contain"
            @error="
              (e) => ((e.target as HTMLImageElement).style.display = 'none')
            "
          />
        </div>
        <UInput
          v-model="company.name"
          :placeholder="$t('clientsCarousel.namePlaceholder')"
          class="flex-1"
        />
        <UInput
          v-model="company.domain"
          :placeholder="$t('clientsCarousel.domainPlaceholder')"
          class="flex-1"
        />
        <UButton
          icon="i-lucide-trash-2"
          color="error"
          variant="ghost"
          size="sm"
          @click="remove(index)"
        />
      </div>
    </div>

    <UButton
      icon="i-lucide-plus"
      variant="outline"
      color="neutral"
      @click="add"
    >
      {{ $t("clientsCarousel.addCompany") }}
    </UButton>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: "dashboard",
  middleware: ["auth", "superuser"],
});

const toast = useToast();
const { t } = useI18n();

type Company = { name: string; domain: string };

const { data } = await useFetch<Company[]>("/content-api/clients-carousel");
const companies = ref<Company[]>(data.value ?? []);

function add() {
  companies.value.push({ name: "", domain: "" });
}

function remove(index: number) {
  companies.value.splice(index, 1);
}

const saving = ref(false);

async function save() {
  saving.value = true;
  try {
    await $fetch("/content-api/clients-carousel", {
      method: "POST",
      body: companies.value,
    });
    toast.add({ title: t("content.saved"), color: "success" });
  } catch {
    toast.add({ title: t("content.saveError"), color: "error" });
  } finally {
    saving.value = false;
  }
}
</script>
