<template>
  <div class="overflow-scroll">
    <UTabs
      :items="tabs"
      variant="link"
      class="w-full"
      :ui="{ trigger: 'grow', list: 'sticky top-0 bg-white z-10' }"
    >
      <template #incoming>
        <UContainer class="flex justify-center">
          <ProjectGrid :items="projects" class="p-4 sm:p-6 w-full max-w-5xl" />
        </UContainer>
      </template>

      <template #search> search </template>
    </UTabs>
  </div>
</template>

<script setup lang="ts">
import type { ProjectPublic } from '~/generated/api';

const projects: ProjectPublic[] = [
  {
    id: '12',
    owner: {
      company_name: 'Company 1',
      logo_url: null,
      email: 'email@example.com',
      location: 'Moscow, Russia',
      role: 'vendor',
      full_name: 'John Doe',
      id: '12345',
    },
    title: 'Custom Software Development',
    budget: 1000,
    start_date: 'Within 60 days',
    description: 'Description of the project',
    services: [
      {
        id: 'f329ebbf-0d65-4919-b0da-1f0016be0b58',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Web Design',
      },
      {
        id: '37c43588-b0f1-4f9b-a1e3-160179eb8d27',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Logo Design',
      },
      {
        id: 'afc10fd1-898a-4ec1-a9a4-c9bcd6f540d0',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Graphic Design',
      },
      {
        id: '13beca1f-f4f3-4777-98cb-8d03711a2b04',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Print Design',
      },
    ],
  },
  {
    id: '12',
    owner: {
      company_name: 'Company 1',
      logo_url: null,
      email: 'email@example.com',
      location: 'Moscow, Russia',
      role: 'vendor',
      full_name: 'John Doe',
      id: '12345',
    },
    title: 'Custom Software Development',
    budget: 1000,
    start_date: 'Within 60 days',
    description: 'Description of the project',
    services: [
      {
        id: 'f329ebbf-0d65-4919-b0da-1f0016be0b58',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Web Design',
      },
      {
        id: '37c43588-b0f1-4f9b-a1e3-160179eb8d27',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Logo Design',
      },
      {
        id: 'afc10fd1-898a-4ec1-a9a4-c9bcd6f540d0',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Graphic Design',
      },
      {
        id: '13beca1f-f4f3-4777-98cb-8d03711a2b04',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Print Design',
      },
    ],
  },
  {
    id: '12',
    owner: {
      company_name: 'Company 1',
      logo_url: null,
      email: 'email@example.com',
      location: 'Moscow, Russia',
      role: 'vendor',
      full_name: 'John Doe',
      id: '12345',
    },
    title: 'Custom Software Development',
    budget: 1000,
    start_date: 'Within 60 days',
    description: 'Description of the project',
    services: [
      {
        id: 'f329ebbf-0d65-4919-b0da-1f0016be0b58',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Web Design',
      },
      {
        id: '37c43588-b0f1-4f9b-a1e3-160179eb8d27',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Logo Design',
      },
      {
        id: 'afc10fd1-898a-4ec1-a9a4-c9bcd6f540d0',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Graphic Design',
      },
      {
        id: '13beca1f-f4f3-4777-98cb-8d03711a2b04',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Print Design',
      },
    ],
  },
  {
    id: '12',
    owner: {
      company_name: 'Company 1',
      logo_url: null,
      email: 'email@example.com',
      location: 'Moscow, Russia',
      role: 'vendor',
      full_name: 'John Doe',
      id: '12345',
    },
    title: 'Custom Software Development',
    budget: 1000,
    start_date: 'Within 60 days',
    description: 'Description of the project',
    services: [
      {
        id: 'f329ebbf-0d65-4919-b0da-1f0016be0b58',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Web Design',
      },
      {
        id: '37c43588-b0f1-4f9b-a1e3-160179eb8d27',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Logo Design',
      },
      {
        id: 'afc10fd1-898a-4ec1-a9a4-c9bcd6f540d0',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Graphic Design',
      },
      {
        id: '13beca1f-f4f3-4777-98cb-8d03711a2b04',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Print Design',
      },
    ],
  },
  {
    id: '12',
    owner: {
      company_name: 'Company 1',
      logo_url: null,
      email: 'email@example.com',
      location: 'Moscow, Russia',
      role: 'vendor',
      full_name: 'John Doe',
      id: '12345',
    },
    title: 'Custom Software Development',
    budget: 1000,
    start_date: 'Within 60 days',
    description: 'Description of the project',
    services: [
      {
        id: 'f329ebbf-0d65-4919-b0da-1f0016be0b58',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Web Design',
      },
      {
        id: '37c43588-b0f1-4f9b-a1e3-160179eb8d27',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Logo Design',
      },
      {
        id: 'afc10fd1-898a-4ec1-a9a4-c9bcd6f540d0',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Graphic Design',
      },
      {
        id: '13beca1f-f4f3-4777-98cb-8d03711a2b04',
        category_id: '537eb2df-7b5c-44db-8530-440eb51e25c0',
        label: 'Print Design',
      },
    ],
  },
];

const tabs = [
  {
    label: 'Incoming Projects',
    icon: 'i-lucide-inbox',
    slot: 'incoming',
  },
  {
    label: 'Find a Project',
    icon: 'i-lucide-compass',
    slot: 'search',
  },
];
</script>
