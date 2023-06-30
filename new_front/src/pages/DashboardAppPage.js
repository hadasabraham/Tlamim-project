import { Helmet } from 'react-helmet-async';
import { faker } from '@faker-js/faker';
import React, { useEffect, useState, Component } from "react";
import { useTheme } from '@mui/material/styles';
import { Grid, Container, Typography } from '@mui/material';
// components
import Iconify from '../components/iconify';
// sections
import {
  AppTasks,
  AppNewsUpdate,
  AppOrderTimeline,
  AppCurrentVisits,
  AppWebsiteVisits,
  AppTrafficBySite,
  AppWidgetSummary,
  AppCurrentSubject,
  AppConversionRates,
} from '../sections/@dashboard/app';

// ----------------------------------------------------------------------

export default function DashboardAppPage() {
  const [data, setData] = useState({ "labels": [], "candidates_by_stages": { "total": [], "active": [], "needs_attention": [] }, active_candidates : [], "need_attention": [] });
  const theme = useTheme();

  const fetchTodos = async (value) => {
    const response = await fetch('http://localhost:8001/statistics')
    const data = await response.json()
    setData(data)
  }

  useEffect(() => {
    fetchTodos();
  }, [])


  return (
    <>
      <Helmet>
        <title> Dashboard | Minimal UI </title>
      </Helmet>

      <Container maxWidth="xl">
        <Typography variant="h4" sx={{ mb: 5 }}>
          Hi, Welcome back
        </Typography>

        <Grid container spacing={3}>
          
          <Grid item xs={12} md={6} lg={8}>
            <AppWebsiteVisits
              title="פילוח שלבים"
              // subheader="(+43%) than last year"
              chartLabels={
                data.candidates_by_stages.labels
              }
              chartData={[
                {
                  name: 'צריכים התייחסות',
                  type: 'column',
                  fill: 'solid',
                  data: data.candidates_by_stages.needs_attention,
                },
                {
                  name: 'הכל',
                  type: 'area',
                  fill: 'gradient',
                  data: data.candidates_by_stages.total,
                },
                {
                  name: 'בתהליך',
                  type: 'line',
                  fill: 'solid',
                  data: data.candidates_by_stages.active,
                },
              ]}
            />
          </Grid>


          <Grid item xs={12} md={6} lg={4}>
            <AppCurrentVisits
              title="חסר התייחסות"
              chartData={
                data.need_attention
              }
              chartColors={[
                theme.palette.primary.main,
                theme.palette.info.main,
                theme.palette.warning.main,
                theme.palette.error.main,
              ]}
            />
          </Grid>

          
          <Grid item xs={12} md={6} lg={4}>
            <AppCurrentVisits
              title="מצב מועמדים"
              chartData={
                data.active_candidates
              }
              chartColors={[
                theme.palette.primary.main,
                theme.palette.info.main,
                theme.palette.warning.main,
                theme.palette.error.main,
              ]}
            />
          </Grid>


          <Grid item xs={12} md={6} lg={4}>
            <AppOrderTimeline
              title="Order Timeline"
              list={[...Array(5)].map((_, index) => ({
                id: faker.datatype.uuid(),
                title: [
                  '1983, orders, $4220',
                  '12 Invoices have been paid',
                  'Order #37745 from September',
                  'New order placed #XF-2356',
                  'New order placed #XF-2346',
                ][index],
                type: `order${index + 1}`,
                time: faker.date.past(),
              }))}
            />
          </Grid>

          <Grid item xs={12} md={6} lg={8}>
            <AppTasks
              title="Tasks"
              list={[
                { id: '1', label: 'Create FireStone Logo' },
                { id: '2', label: 'Add SCSS and JS files if required' },
                { id: '3', label: 'Stakeholder Meeting' },
                { id: '4', label: 'Scoping & Estimations' },
                { id: '5', label: 'Sprint Showcase' },
              ]}
            />
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
